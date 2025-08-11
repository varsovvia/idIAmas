# 🎯 idIAmas - Italian Subtitle Translator & Language Learning

A powerful, real-time Italian subtitle translator that helps you learn Italian while watching movies, TV shows, or any video content. **Now with a beautiful, modern desktop popup interface!**

## ✨ Features

- **🎬 Real-time Subtitle Capture** - Automatically captures subtitles from your screen
- **🤖 AI-Powered Translation** - Uses OpenAI GPT-3.5-turbo for accurate translations
- **📚 Comprehensive Grammar Explanations** - Learn Italian grammar word by word
- **🎨 Modern Desktop Popup** - Beautiful, professional interface that appears over your content
- **⌨️ Hotkey Activation** - Press 'i' to translate, 'q' or 'Esc' to exit
- **📱 Always on Top** - Popup stays visible while you continue watching
- **📋 Copy to Clipboard** - Easy copying of translations and explanations
- **🎯 Drag & Drop** - Move the popup anywhere on your screen
- **🌙 Dark Theme** - Easy on the eyes for extended use

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Tesseract OCR** installed for text extraction
3. **OpenAI API Key** for AI-powered translations

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/varsovvia/idIAmas.git
   cd idIAmas
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR:**
   - **Windows:** Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS:** `brew install tesseract`
   - **Linux:** `sudo apt install tesseract-ocr`

4. **Configure your OpenAI API key:**
   ```bash
   python setup.py
   ```

### Usage

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Position your video content** so subtitles are in the capture region

3. **Press 'i'** when you want to translate subtitles

4. **Enjoy the beautiful popup** with translations and grammar explanations!

5. **Press 'q' or 'Esc'** to exit

## 🎨 Modern Desktop Popup

The new interface features:

- **Professional Design** - Clean, modern appearance similar to business applications
- **Tabbed Interface** - Organized sections for Original, Translation, and Grammar
- **Always on Top** - Stays visible while you continue watching
- **Draggable** - Move it anywhere on your screen
- **Copy Buttons** - Easy copying of any content
- **Smooth Animations** - Beautiful entrance and exit effects
- **Responsive Layout** - Adapts to different content lengths

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Screen Region for Subtitles (x, y, width, height)
SUBTITLES_REGION=150,750,1520,330

# OpenAI Model Settings
OPENAI_MODEL=gpt-3.5-turbo
MAX_TOKENS=500
TEMPERATURE=0.7

# OCR Settings
OCR_LANGUAGE=ita
IMAGE_THRESHOLD=200
```

### Screen Region Setup

The `SUBTITLES_REGION` defines where subtitles appear on your screen:
- **Format:** `x,y,width,height`
- **Default:** `150,750,1520,330` (bottom center area)
- **Adjust** based on your screen resolution and video player

## 🏗️ Architecture

- **PyQt6** - Modern desktop GUI framework
- **OpenAI GPT-3.5-turbo** - AI-powered translation and explanations
- **Tesseract OCR** - Text extraction from images
- **PyAutoGUI** - Screen capture functionality
- **Pynput** - Keyboard hotkey listening

## 📱 How It Works

1. **Screen Capture** - Captures the specified region when you press 'i'
2. **OCR Processing** - Extracts Italian text using Tesseract
3. **AI Translation** - Sends text to OpenAI for translation and grammar explanation
4. **Modern Popup** - Displays results in a beautiful, organized interface
5. **Learning** - Study grammar explanations and improve your Italian!

## 🎯 Learning Features

- **Word-by-word explanations** of Italian grammar
- **Function identification** (verb, noun, preposition, etc.)
- **Common expressions** and contractions
- **Beginner-friendly** explanations
- **Structured learning** with organized tabs

## 🛠️ Troubleshooting

### Common Issues

1. **"No text detected"**
   - Adjust `SUBTITLES_REGION` coordinates
   - Ensure subtitles are visible and clear
   - Check Tesseract installation

2. **"API key not found"**
   - Run `python setup.py` to configure
   - Check your `.env` file
   - Verify environment variables

3. **Popup not appearing**
   - Ensure PyQt6 is installed: `pip install PyQt6`
   - Check for error messages in console
   - Verify screen resolution compatibility

### Performance Tips

- **Optimize screen region** to capture only subtitle area
- **Adjust image threshold** for better OCR accuracy
- **Use appropriate language** for your content (ita, eng, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for powerful language models
- **Tesseract** for OCR capabilities
- **PyQt6** for modern desktop interface
- **Italian language learners** for inspiration

---

**🎯 Start learning Italian today with idIAmas!**

Press 'i' to translate, 'q' to quit, and enjoy your language learning journey! 🇮🇹✨
