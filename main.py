import pyautogui
import pytesseract
from PIL import Image
from openai import OpenAI
from pynput import keyboard

from validation import parse_and_validate_translation
from popup_launcher import launch_popup_subprocess
from utilidades import save_image
import time
import os
import logging
from typing import Optional, Tuple
import json
from dataclasses import dataclass
from io import BytesIO
import re

    # Try to load dotenv for .env file support
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger = logging.getLogger(__name__)
    logger.info("Loaded environment variables from .env file")
except ImportError:
    logger = logging.getLogger(__name__)
    logger.info("python-dotenv not installed, using system environment variables only")

# Configure logging with optional timings-only mode
TIMINGS_ONLY = os.getenv('TIMINGS_ONLY', '0') == '1'

_handlers = [logging.FileHandler('app.log')]
if not TIMINGS_ONLY:
    _handlers.append(logging.StreamHandler())

logging.basicConfig(
    level=logging.ERROR if TIMINGS_ONLY else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=_handlers,
)
logger = logging.getLogger(__name__)

@dataclass
class Config:
    """Configuration class for the application"""
    # Optimized region: focus on subtitle area, avoid UI elements
    # Format: (left, top, width, height) - adjusted to capture mainly subtitle text
    subtitles_region: Tuple[int, int, int, int] = (150, 850, 1520, 120)  # Much smaller height, moved further down
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini"  # Faster than gpt-3.5-turbo
    max_tokens: int = 800        # Increased from 250 to allow more grammar explanations
    temperature: float = 0.3     # Lower for more predictable, faster responses
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
        
        # Performance optimization: simple cache for common words
        self.word_cache = {
            "ciao": {"translation": "hola", "grammar": [{"word": "ciao", "explanation": "saludo informal", "function": "interjección"}]},
            "grazie": {"translation": "gracias", "grammar": [{"word": "grazie", "explanation": "expresión de agradecimiento", "function": "interjección"}]},
            "prego": {"translation": "de nada", "grammar": [{"word": "prego", "explanation": "respuesta a gracias", "function": "interjección"}]},
        }
    
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
        """Extract text from image with optimized preprocessing for speed and subtitle filtering"""
        try:
            # Convert to grayscale (faster than full color processing)
            imagen = imagen.convert("L")
            
            # Crop to focus only on the center subtitle area (avoid edges where metadata might be)
            width, height = imagen.size
            # Focus on center 60% of width and height to avoid edge metadata
            left = int(width * 0.2)  # 20% from left
            top = int(height * 0.2)   # 20% from top
            right = int(width * 0.8)  # 80% from left
            bottom = int(height * 0.8) # 80% from top
            
            imagen = imagen.crop((left, top, right, bottom))
            
            # Optimized threshold for faster processing (reduced from 200)
            threshold = min(self.config.threshold, 150)  # Use lower threshold for speed
            imagen = imagen.point(lambda x: 0 if x < threshold else 255, '1')
            
            # Extract text with optimized OCR settings
            texto = pytesseract.image_to_string(
                imagen, 
                lang=self.config.ocr_language,
                config='--oem 1 --psm 6'  # Fast OCR mode
            ).strip()
            
            if not texto:
                logger.warning("No text detected in image")
                return ""
            
            # Clean and filter the extracted text to focus on subtitles
            texto_limpio = self._limpiar_texto_subtitulos(texto)
            logger.info(f"Text extracted: {texto[:50]}...")
            logger.info(f"Cleaned text: {texto_limpio}")
            return texto_limpio
            
        except Exception as e:
            logger.error(f"Failed to extract text: {e}")
            return ""
    
    def _limpiar_texto_subtitulos(self, texto: str) -> str:
        """Clean extracted text to focus only on subtitle content"""
        if not texto:
            return ""
        
        if not TIMINGS_ONLY:
            print(f"🔍 Raw OCR text: {texto}")
        
        # Split into lines and process each one
        lineas = texto.split('\n')
        lineas_limpias = []
        
        for i, linea in enumerate(lineas):
            linea = linea.strip()
            if not linea:
                continue
            
            if not TIMINGS_ONLY:
                print(f"📝 Line {i}: '{linea}'")
            
            # Simple filtering: keep lines that look like actual dialogue
            if self._es_linea_subtitulo_simple(linea):
                if not TIMINGS_ONLY:
                    print(f"✅ Keeping line: '{linea}'")
                lineas_limpias.append(linea)
            else:
                if not TIMINGS_ONLY:
                    print(f"❌ Filtering out line: '{linea}'")
        
        # Join clean lines
        resultado = '\n'.join(lineas_limpias)
        if not TIMINGS_ONLY:
            print(f"🧹 Cleaned result: {resultado}")
        
        return resultado.strip()
    
    def _es_linea_subtitulo_simple(self, linea: str) -> bool:
        """Simple check if a line looks like subtitle dialogue"""
        linea = linea.strip()
        
        # Skip empty lines
        if not linea:
            return False
        
        # Skip lines that are too short (likely UI elements)
        if len(linea) < 3:
            return False
        
        # Skip lines that are mostly numbers or symbols
        letter_count = len(re.findall(r'[a-zA-Z]', linea))
        if letter_count < len(linea) * 0.3:  # At least 30% should be letters
            return False
        
        # Skip lines that are just technical codes
        if re.match(r'^[A-Z]{2,}\s*[\d\(\)\s]+$', linea):
            return False
        
        # Skip lines that contain technical metadata patterns
        if re.search(r'[A-Z]{2,}\s+\d+', linea):  # Like "Baby E1"
            return False
        
        # Skip lines that contain episode identifiers
        if re.search(r'[A-Z][a-z]+\s+E\d+', linea):  # Like "Baby E1"
            return False
        
        # Skip lines that contain technical codes with metadata
        if re.search(r'[A-Z]{2,}\s*\(?\s*\d+', linea):  # Like "DI (105"
            return False
        
        # Skip lines that contain mostly technical codes and show names
        if re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+', linea) and len(linea) < 20:
            return False
        
        # Skip lines that contain technical symbols like | = etc.
        if re.search(r'[|=\-\+\*]', linea) and len(linea) < 25:
            return False
        
        # If we get here, it's likely a subtitle line
        return True
    
    def translate_text_with_explanation(self, texto: str) -> str:
        """Translate text with comprehensive error handling"""
        if not texto:
            return "No text detected in the image."
        
        if not self.client:
            return "Error: OpenAI API key not configured."
        
        # Performance optimization: check cache first
        texto_lower = texto.lower().strip()
        if texto_lower in self.word_cache:
            cached_result = self.word_cache[texto_lower]
            if os.getenv('DEBUG', '0') == '1':
                logger.info("Cache hit for %s - skipping API call", texto_lower)
            return json.dumps({
                "original": texto,
                "translation": cached_result["translation"],
                "grammar": cached_result["grammar"]
            }, ensure_ascii=False)
        
        try:
            # Dynamic language selection for explanations
            explanation_lang = self.config.explanation_language
            target_lang = "Spanish" if explanation_lang == "spanish" else explanation_lang.title()
            
            # Strict JSON output instruction to simplify parsing downstream
            prompt = (
                "Traduce del italiano al español y devuelve JSON:\n"
                "{\n"
                "  \"original\": \"<texto italiano>\",\n"
                "  \"translation\": \"<traducción español>\",\n"
                "  \"grammar\": [\n"
                "    {\n"
                "      \"word\": \"<palabra>\",\n"
                "      \"explanation\": \"<significado>\",\n"
                "      \"function\": \"<función gramatical>\",\n"
                "      \"additional_info\": \"<información adicional como conjugación, género, número>\",\n"
                "      \"examples\": \"<ejemplos de uso en contexto>\",\n"
                "      \"difficulty\": \"<nivel de dificultad: básico/intermedio/avanzado>\"\n"
                "    }\n"
                "  ]\n"
                "}\n\n"
                "IMPORTANTE: Analiza TODAS las palabras importantes del texto italiano. "
                "Incluye verbos, sustantivos, pronombres, artículos, preposiciones y otras palabras gramaticalmente relevantes. "
                "Para cada palabra, proporciona:\n"
                "- Función gramatical detallada\n"
                "- Información adicional (conjugación, género, número, etc.)\n"
                "- Ejemplos de uso en contexto\n"
                "- Nivel de dificultad\n"
                "No solo traduzcas, sino que expliques la función gramatical de cada palabra importante.\n\n"
                f"Texto: {texto}"
            )

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en gramática italiana y enseñanza de idiomas. Tu tarea es: 1) Traducir del italiano al español, 2) Analizar TODAS las palabras importantes explicando su función gramatical detallada, conjugación, género, número, ejemplos de uso y nivel de dificultad en español. Responde SOLO en JSON."},
                    {"role": "user", "content": prompt},
                ],
                # Force valid JSON to reduce parsing overhead and avoid code fences
                response_format={"type": "json_object"},
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            
            result = response.choices[0].message.content.strip()

            # Normalize output to a clean JSON string if possible
            def _extract_json_block(s: str) -> str:
                s = s.strip()
                # Remove common markdown fences
                if s.startswith('```'):
                    s = s.strip('`')
                # Extract the substring between the first '{' and the last '}'
                start = s.find('{')
                end = s.rfind('}')
                if start != -1 and end != -1 and end > start:
                    return s[start:end+1]
                return s

            cleaned = _extract_json_block(result)
            try:
                parsed = json.loads(cleaned)
                # Ensure keys exist and dump canonical JSON with unicode preserved
                normalized = {
                    "original": parsed.get("original", ""),
                    "translation": parsed.get("translation", ""),
                    "grammar": parsed.get("grammar", []),
                }
                result = json.dumps(normalized, ensure_ascii=False)
            except Exception:
                # Keep original non-JSON response as fallback
                pass
            
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
        t0 = time.perf_counter()
        
        try:
            logger.info("Starting translation workflow...")
            
            # Capture subtitles
            imagen = self.captura_subtitulos()
            if imagen is None:
                logger.error("Failed to capture image")
                return False
            t1 = time.perf_counter()
            capture_duration = t1 - t0
            if os.getenv('DEBUG', '0') == '1':
                logger.info("Image capture completed in %.2f seconds", capture_duration)
            
            # Extract text
            texto = self.extraer_texto(imagen)
            if not texto:
                logger.warning("No text to translate")
                return False
            t2 = time.perf_counter()
            ocr_duration = t2 - t1
            if os.getenv('DEBUG', '0') == '1':
                logger.info("Text extraction completed in %.2f seconds", ocr_duration)
            
            # Translate
            translation = self.translate_text_with_explanation(texto)
            t3 = time.perf_counter()
            translation_duration = t3 - t2
            total_duration = t3 - t0
            logger.info("Translation workflow completed in %.2f seconds", total_duration)

            if TIMINGS_ONLY:
                print(
                    f"Timings | Capture: {capture_duration:.3f}s | OCR: {ocr_duration:.3f}s | "
                    f"Translate: {translation_duration:.3f}s | Total: {total_duration:.3f}s"
                )
            
            # Show results in modern desktop popup
            validated = parse_and_validate_translation(translation)
            launch_popup_subprocess(validated)
            # Avoid disk I/O unless debugging
            if os.getenv('DEBUG', '0') == '1':
                save_image(imagen)
            
            return True
            
        except Exception as e:
            logger.error(f"Translation workflow failed: {e}")
            return False

def load_config() -> Config:
    """Load configuration from environment variables"""
    return Config(
        api_key=os.getenv('OPENAI_API_KEY'),
        subtitles_region=tuple(map(int, os.getenv('SUBTITLES_REGION', '150,800,1520,200').split(','))),
        model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        max_tokens=int(os.getenv('MAX_TOKENS', '800')),  # Increased default
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
        

        
        if TIMINGS_ONLY:
            print("Ready. Press 'i' to translate; 'q' or 'Esc' to exit.")
        else:
            print("Listener started. Press 'i' to translate, 'q' or 'Esc' to exit.")
        logger.info("Application started successfully")
        
        with keyboard.Listener(on_press=lambda key: on_press(translator, key)) as listener:
            listener.join()
            
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
