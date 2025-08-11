import pyautogui
import pytesseract
from PIL import Image
from openai import OpenAI
from pynput import keyboard

from modern_popup_pyqt6 import mostrar_explicacion_moderna_pyqt6
from utilidades import save_image
import time
import os
import logging
from typing import Optional, Tuple
from dataclasses import dataclass
from io import BytesIO

    # Try to load dotenv for .env file support
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger = logging.getLogger(__name__)
    logger.info("Loaded environment variables from .env file")
except ImportError:
    logger = logging.getLogger(__name__)
    logger.info("python-dotenv not installed, using system environment variables only")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Config:
    """Configuration class for the application"""
    subtitles_region: Tuple[int, int, int, int] = (150, 750, 1520, 330)
    api_key: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7
    ocr_language: str = 'ita'  # Language for OCR (source text)
    explanation_language: str = 'spanish'  # Language for explanations
    threshold: int = 200

class SubtitleTranslator:
    """Main class for subtitle translation functionality"""
    
    def __init__(self, config: Config):
        self.config = config
        self._validate_config()
        self.client = OpenAI(api_key=config.api_key) if config.api_key else None
        self.translation_history = []
        
    def _validate_config(self):
        """Validate configuration settings"""
        if not self.config.api_key:
            logger.warning("No API key provided. Translation features will be disabled.")
        if not all(isinstance(x, int) and x >= 0 for x in self.config.subtitles_region):
            raise ValueError("Invalid subtitles region coordinates")
    
    def captura_subtitulos(self) -> Optional[Image.Image]:
        """Capture subtitles from screen with error handling"""
        try:
            logger.info("Capturing subtitles from screen...")
            screenshot = pyautogui.screenshot(region=self.config.subtitles_region)
            logger.info("Screenshot captured successfully")
            return screenshot
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None
    
    def extraer_texto(self, imagen: Image.Image) -> str:
        """Extract text from image with improved preprocessing"""
        try:
            # Convert to grayscale
            imagen = imagen.convert("L")
            
            # Apply threshold for better OCR
            imagen = imagen.point(lambda x: 0 if x < self.config.threshold else 255, '1')
            
            # Extract text
            texto = pytesseract.image_to_string(imagen, lang=self.config.ocr_language).strip()
            
            if not texto:
                logger.warning("No text detected in image")
                return ""
                
            logger.info(f"Text extracted: {texto[:50]}...")
            return texto
            
        except Exception as e:
            logger.error(f"Failed to extract text: {e}")
            return ""
    
    def translate_text_with_explanation(self, texto: str) -> str:
        """Translate text with comprehensive error handling"""
        if not texto:
            return "No text detected in the image."
        
        if not self.client:
            return "Error: OpenAI API key not configured."
        
        try:
            # Dynamic language selection for explanations
            explanation_lang = self.config.explanation_language
            target_lang = "Spanish" if explanation_lang == "spanish" else explanation_lang.title()
            
            prompt = (
                f"Translate the following Italian text and provide a complete explanation in {target_lang}. "
                f"Format your response exactly as follows:\n\n"
                f"ORIGINAL TEXT:\n"
                f"[Write the Italian text exactly as received]\n\n"
                f"TRANSLATION TO {target_lang.upper()}:\n"
                f"[Clear and natural translation to {target_lang}]\n\n"
                f"GRAMMAR EXPLANATION:\n"
                f"[Explain each important word or phrase, its grammatical function and meaning. "
                f"Be clear and educational for a beginner]\n\n"
                f"Text to translate: {texto}\n\n"
                f"Response:"
            )

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": f"You are an Italian teacher for beginners. You receive Italian phrases from subtitles. "
                    f"Your task is:\n"
                    f"1. Rewrite the Italian phrase exactly as received (ORIGINAL TEXT)\n"
                    f"2. Translate it to {target_lang} with the same meaning (TRANSLATION TO {target_lang.upper()})\n"
                    f"3. Explain each important word in the phrase (GRAMMAR EXPLANATION):\n"
                    f"   - meaning in {target_lang}\n"
                    f"   - grammatical function (verb, noun, preposition...)\n"
                    f"   - notes about contractions, conjugations or common expressions\n"
                    f"4. Use the exact format specified in the prompt\n"
                    f"Be clear, patient and direct, as if the reader knows nothing yet."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            
            result = response.choices[0].message.content.strip()
            
            # Save to history
            self.translation_history.append({
                'original': texto,
                'translation': result,
                'timestamp': time.time()
            })
            
            logger.info("Translation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return f"Translation error: {str(e)}"
    
    def execute_translation(self) -> bool:
        """Execute complete translation workflow with timing and error handling"""
        start_time = time.time()
        
        try:
            logger.info("Starting translation workflow...")
            
            # Capture subtitles
            imagen = self.captura_subtitulos()
            if imagen is None:
                logger.error("Failed to capture image")
                return False
                
            capture_time = time.time() - start_time
            logger.info(f"Image capture completed in {capture_time:.2f} seconds")
            
            # Extract text
            texto = self.extraer_texto(imagen)
            if not texto:
                logger.warning("No text to translate")
                return False
                
            extraction_time = time.time() - start_time
            logger.info(f"Text extraction completed in {extraction_time:.2f} seconds")
            
            # Translate
            translation = self.translate_text_with_explanation(texto)
            total_time = time.time() - start_time
            logger.info(f"Translation workflow completed in {total_time:.2f} seconds")
            
            # Show results in modern desktop popup
            mostrar_explicacion_moderna_pyqt6(translation)
            save_image(imagen)
            
            return True
            
        except Exception as e:
            logger.error(f"Translation workflow failed: {e}")
            return False

def load_config() -> Config:
    """Load configuration from environment variables"""
    return Config(
        api_key=os.getenv('OPENAI_API_KEY'),
        subtitles_region=tuple(map(int, os.getenv('SUBTITLES_REGION', '150,750,1520,330').split(','))),
        model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        max_tokens=int(os.getenv('MAX_TOKENS', '500')),
        temperature=float(os.getenv('TEMPERATURE', '0.7')),
        ocr_language=os.getenv('OCR_LANGUAGE', 'ita'),
        explanation_language=os.getenv('EXPLANATION_LANGUAGE', 'spanish'),
        threshold=int(os.getenv('IMAGE_THRESHOLD', '200'))
    )

def on_press(translator: SubtitleTranslator, key):
    """Handle keyboard input with error handling"""
    try:
        if key.char == 'i':
            logger.info("Translation requested via hotkey")
            success = translator.execute_translation()
            if not success:
                logger.error("Translation failed")
        elif key.char == 'q':
            logger.info("Exit requested via hotkey")
            return False
    except AttributeError:
        if key == keyboard.Key.esc:
            logger.info("Exit requested via ESC key")
            return False
    except Exception as e:
        logger.error(f"Error in key handler: {e}")

def main():
    """Main application entry point"""
    try:
        # Load configuration
        config = load_config()
        
        if not config.api_key:
            logger.error("No OpenAI API key found. Please set OPENAI_API_KEY environment variable.")
            print("❌ Error: No OpenAI API key configured!")
            print("\n🔧 Quick Setup Options:")
            print("   1. Run the setup wizard: python setup.py")
            print("   2. Create a .env file with your API key")
            print("   3. Set OPENAI_API_KEY environment variable")
            print("\n📚 For detailed instructions, see CONFIGURATION.md")
            print("🔑 Get your API key from: https://platform.openai.com/api-keys")
            return
        
        # Initialize translator
        translator = SubtitleTranslator(config)
        
        print("Listener started. Press 'i' to translate, 'q' or 'Esc' to exit.")
        logger.info("Application started successfully")
        
        with keyboard.Listener(on_press=lambda key: on_press(translator, key)) as listener:
            listener.join()
            
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
