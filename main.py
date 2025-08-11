import pyautogui
import pytesseract
from PIL import Image
from openai import OpenAI
from pynput import keyboard
import tkinter as tk
from test_tinkter import mostrar_explicacion
from utilidades import guardar_imagen
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
    language: str = 'ita'
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
            texto = pytesseract.image_to_string(imagen, lang=self.config.language).strip()
            
            if not texto:
                logger.warning("No text detected in image")
                return ""
                
            logger.info(f"Text extracted: {texto[:50]}...")
            return texto
            
        except Exception as e:
            logger.error(f"Failed to extract text: {e}")
            return ""
    
    def traducir_texto_con_explicacion(self, texto: str) -> str:
        """Translate text with comprehensive error handling"""
        if not texto:
            return "No se detectó texto en la imagen."
        
        if not self.client:
            return "Error: No se ha configurado la API key de OpenAI."
        
        try:
            prompt = (
                f"Traduce el siguiente texto italiano y proporciona una explicación completa en español. "
                f"Formatea tu respuesta de la siguiente manera:\n\n"
                f"TEXTO ORIGINAL:\n"
                f"[Escribe aquí el texto italiano tal como fue recibido]\n\n"
                f"TRADUCCIÓN AL ESPAÑOL:\n"
                f"[Traducción clara y natural al español]\n\n"
                f"EXPLICACIÓN GRAMATICAL:\n"
                f"[Explica cada palabra o frase importante, su función gramatical y significado. "
                f"Sé claro y educativo para un principiante]\n\n"
                f"Texto a traducir: {texto}\n\n"
                f"Respuesta:"
            )

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "Eres un profesor de italiano para principiantes. Recibes frases en italiano sacadas de subtítulos. "
                    "Tu tarea es:\n"
                    "1. Reescribir la frase en italiano tal como fue recibida (TEXTO ORIGINAL)\n"
                    "2. Traducirla al español con el mismo sentido (TRADUCCIÓN AL ESPAÑOL)\n"
                    "3. Explicar cada palabra importante en la frase (EXPLICACIÓN GRAMATICAL):\n"
                    "   - significado en español\n"
                    "   - función gramatical (verbo, sustantivo, preposición...)\n"
                    "   - notas si hay contracciones, conjugaciones o expresiones comunes\n"
                    "4. Usa el formato exacto especificado en el prompt\n"
                    "Sé claro, paciente y directo, como si el lector no supiera nada aún."},
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
            return f"Error en la traducción: {str(e)}"
    
    def ejecutar_traduccion(self) -> bool:
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
            traduccion = self.traducir_texto_con_explicacion(texto)
            total_time = time.time() - start_time
            logger.info(f"Translation workflow completed in {total_time:.2f} seconds")
            
            # Show results
            mostrar_explicacion(traduccion)
            guardar_imagen(imagen)
            
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
        language=os.getenv('OCR_LANGUAGE', 'ita'),
        threshold=int(os.getenv('IMAGE_THRESHOLD', '200'))
    )

def on_press(translator: SubtitleTranslator, key):
    """Handle keyboard input with error handling"""
    try:
        if key.char == 'i':
            logger.info("Translation requested via hotkey")
            success = translator.ejecutar_traduccion()
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
        
        print("Listener iniciado. Pulsa la tecla 'i' para traducir, 'q' o 'Esc' para salir.")
        logger.info("Application started successfully")
        
        with keyboard.Listener(on_press=lambda key: on_press(translator, key)) as listener:
            listener.join()
            
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
