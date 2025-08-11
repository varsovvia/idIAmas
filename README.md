# idIAmas - Italian Subtitle Translator & Language Learning Tool

A real-time Italian subtitle translation and language learning application that captures subtitles from your screen and provides detailed translations with grammatical explanations.

## Features

- **Real-time subtitle capture** from any video player
- **AI-powered translation** using OpenAI GPT models
- **Comprehensive language learning** with word-by-word explanations
- **Grammar analysis** and educational content
- **Hotkey activation** for seamless use while watching content
- **Translation history** tracking
- **Configurable screen regions** for different subtitle positions

## Security Improvements

- ✅ **No hardcoded API keys** - uses environment variables
- ✅ **Comprehensive error handling** throughout the application
- ✅ **Input validation** and sanitization
- ✅ **Logging system** for debugging and monitoring
- ✅ **Graceful failure handling** for all operations

## Installation

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Tesseract OCR** installed and accessible in your PATH
3. **OpenAI API key** for translation services

### Install Tesseract OCR

#### Windows:
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Or use chocolatey:
choco install tesseract
```

#### macOS:
```bash
brew install tesseract
```

#### Linux:
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-ita  # Italian language pack
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Set Environment Variables

Create a `.env` file in the project directory or set system environment variables:

```bash
# Required
OPENAI_API_KEY=your_actual_api_key_here

# Optional (with defaults)
SUBTITLES_REGION=150,750,1520,330
OPENAI_MODEL=gpt-3.5-turbo
MAX_TOKENS=500
TEMPERATURE=0.7
OCR_LANGUAGE=ita
IMAGE_THRESHOLD=200
```

### 2. Configure Screen Region

The `SUBTITLES_REGION` format is `(x, y, width, height)`:
- **x, y**: Top-left corner coordinates
- **width, height**: Dimensions of the capture area

Adjust these values based on your screen resolution and where subtitles appear.

## Usage

### Basic Usage

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Position your video player** so subtitles are in the configured region

3. **Press 'i'** to capture and translate subtitles

4. **Press 'q' or 'Esc'** to exit

### Advanced Usage

- **Custom screen regions**: Modify `SUBTITLES_REGION` in environment variables
- **Different languages**: Change `OCR_LANGUAGE` for other subtitle languages
- **Model customization**: Adjust `TEMPERATURE` and `MAX_TOKENS` for different AI responses

## How It Works

1. **Screen Capture**: Takes a screenshot of the configured subtitle region
2. **OCR Processing**: Extracts text using Tesseract with Italian language support
3. **AI Translation**: Sends text to OpenAI GPT for translation and explanation
4. **Learning Content**: Provides detailed grammatical analysis and word explanations
5. **Display**: Shows results in a user-friendly interface

## Troubleshooting

### Common Issues

1. **"No OpenAI API key found"**
   - Set the `OPENAI_API_KEY` environment variable
   - Ensure the API key is valid and has credits

2. **"Failed to capture screenshot"**
   - Check if the `SUBTITLES_REGION` coordinates are correct
   - Ensure the application has screen capture permissions

3. **"No text detected"**
   - Adjust the `IMAGE_THRESHOLD` value
   - Check if subtitles are clearly visible in the capture region
   - Verify Tesseract is properly installed

4. **Poor OCR accuracy**
   - Increase `IMAGE_THRESHOLD` for darker text
   - Decrease for lighter text
   - Ensure good contrast between text and background

### Logs

The application creates detailed logs in `app.log` for debugging:
```bash
tail -f app.log  # Monitor logs in real-time
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
