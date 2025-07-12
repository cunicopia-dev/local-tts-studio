# 🎙️ Local TTS Studio

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)](https://github.com/yourusername/local-tts-studio)
[![TTS Engine](https://img.shields.io/badge/TTS-XTTS--v2-green.svg)](https://huggingface.co/coqui/XTTS-v2)
[![Audio](https://img.shields.io/badge/audio-WAV%20%7C%20MP3-orange.svg)](https://github.com/yourusername/local-tts-studio)

> 🚀 **Professional offline text-to-speech studio with voice cloning capabilities**
> 
> Transform books, documents, and any text into natural-sounding audiobooks using state-of-the-art XTTS-v2 technology. No internet required, complete privacy, professional results.

---

## 📋 Table of Contents

- [✨ Key Features](#-key-features)
- [🚀 Installation](#-installation)
- [🎯 Usage Guide](#-usage-guide)
- [🏗️ Architecture](#️-architecture)
- [🎵 Voice Cloning Guide](#-voice-cloning-guide)
- [🛠️ Smart Text Processing](#️-smart-text-processing)
- [⚙️ Configuration & Settings](#️-configuration--settings)
- [🚨 Troubleshooting](#-troubleshooting)
- [🔗 What Makes This Interesting](#-what-makes-this-interesting)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

## ✨ Key Features

### 🎯 **Smart Text Processing**
- **Automatic Text Cleaning**: Removes emojis, fixes problematic characters, normalizes line endings
- **Multi-format Support**: Load TXT, MD, and PDF files with automatic preprocessing
- **Intelligent Character Replacement**: Converts symbols to speech-friendly text (™→"trademark", €→"euros")
- **Line Ending Normalization**: Handles CRLF/LF issues automatically

### 🎤 **Advanced Audio Generation**
- **Voice Cloning**: Clone any voice from a WAV sample using XTTS-v2
- **Streaming Playback**: Hear results immediately as synthesis progresses
- **Professional Quality**: State-of-the-art neural TTS with natural prosody
- **Export Options**: Save as WAV or MP3 with configurable quality

### 💻 **Text Editor**
- **Standard Shortcuts**: Ctrl+A (select all), Ctrl+F (find/replace), Ctrl+Z/Y (undo/redo)
- **Find & Replace**: Advanced search with regex support
- **Smart Preprocessing**: One-click text cleaning for optimal TTS results
- **Undo Support**: Restore original text after cleaning operations

### 🚀 **Performance & Usability**
- **Streaming Architecture**: Start hearing audio within seconds, not minutes
- **Chunked Processing**: Efficiently handle large documents (books, reports)
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Dual Interface**: Both GUI and CLI for different workflows
- **Professional UX**: Progress tracking, status updates, and error handling

## 🚀 Installation

### 📋 Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | 3.8-3.11 | 3.12+ not yet supported by TTS dependencies |
| **FFmpeg** | Latest | Required for audio processing |
| **GPU** | CUDA-compatible | Optional, but 5-10x faster than CPU |

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### ⚡ Quick Start

**1. Clone and setup:**
```bash
git clone https://github.com/yourusername/local-tts-studio.git
cd local-tts-studio
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Launch GUI:**
```bash
python run.py
```

**3. Start creating:** Load a document, optionally load a voice sample, and click "Speak"!

> 💡 **First run**: The app will automatically download the XTTS-v2 model (~1.8GB) on first use.

## 🎯 Usage Guide

### GUI Mode (Recommended)

**Launch the application**:
```bash
python run.py
```

**🔄 Workflow:**

```
📄 Load Content → 🎤 Load Voice (optional) → ▶️ Generate → 💾 Save Audio
```

1. **📂 Load Content**: File → Open Text/PDF (automatically cleaned)
2. **🎤 Optional Voice**: Voice → Load Voice Sample (for cloning)  
3. **▶️ Generate**: Click "Speak" (streaming playback starts immediately)
4. **💾 Save**: Click "Save Audio" to export WAV/MP3

**Text Editor Features**:
- **Ctrl+A**: Select all text
- **Ctrl+F**: Find and replace with regex support
- **Edit → Clean Text for TTS**: Manual text cleaning
- **Edit → Undo Text Cleaning**: Restore original text

### 💻 Command-Line Mode

**Basic conversion:**
```bash
python tts_cli.py convert input.txt output.wav
```

**With voice cloning:**
```bash
python tts_cli.py convert book.pdf audiobook.mp3 --voice voice_sample.wav
```

**⚙️ CLI Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--voice, -v` | WAV file for voice cloning | Built-in voice |
| `--chunk-size, -c` | Max characters per chunk | 200 |
| `--gpu` | Enable GPU acceleration | Auto-detect |
| `--verbose` | Enable detailed logging | False |

### 📚 Examples

```bash
# 📖 Convert a PDF to MP3 with custom voice
python tts_cli.py convert manual.pdf manual_audio.mp3 --voice john.wav --gpu

# 📝 Convert markdown to WAV  
python tts_cli.py convert README.md readme_audio.wav

# 📕 Process large book with optimized chunks
python tts_cli.py convert large_book.txt book.mp3 --chunk-size 150
```

## 🏗️ Architecture

Built with professional software engineering practices:

```
local-tts-studio/
├── src/
│   ├── core/
│   │   └── tts_engine.py           # TTS synthesis engine
│   ├── gui/
│   │   ├── main_window.py          # Main application GUI
│   │   └── text_editor_enhancements.py  # Advanced text editing
│   ├── utils/
│   │   ├── text_processing.py      # File loading and chunking
│   │   ├── text_preprocessing.py   # Smart text cleaning pipeline
│   │   └── audio_utils.py          # Streaming audio playback
│   └── config/
│       └── settings.py             # Configuration management
├── tests/                          # Unit tests
├── run.py                          # GUI entry point
├── tts_cli.py                     # CLI interface
└── requirements.txt               # Python dependencies
```

### Key Design Principles
- **Modular Architecture**: Separate concerns for maintainability
- **Streaming Processing**: Real-time audio generation and playback
- **Professional UX**: Standard shortcuts, progress feedback, error handling
- **Intelligent Preprocessing**: Automatic text optimization for TTS
- **Cross-Platform**: Works on Windows, macOS, Linux

## 🎵 Voice Cloning Guide

### Getting Great Results
1. **Quality Recording**: Use a clear WAV file (10-30 seconds)
2. **Clean Audio**: Minimal background noise, consistent volume
3. **Natural Speech**: Include varied intonation and speech patterns
4. **Technical Specs**: 22050 Hz sample rate or higher recommended

### Tips for Success
- **Avoid monotone**: Include questions, statements, excitement
- **Multiple sentences**: Better than single words or phrases
- **Clear articulation**: Avoid mumbling or unclear speech
- **Consistent quality**: Same microphone/environment if possible

## 🛠️ Smart Text Processing

Local TTS Studio automatically handles problematic text elements:

### Automatic Cleaning
- **Emojis**: 😀🎉🚀 → Removed completely
- **Special Characters**: ™€£ → "trademark euros pounds"
- **Smart Quotes**: ""'' → Regular quotes
- **Line Endings**: CRLF/LF → Normalized
- **URLs/Emails**: → "web link" / "email address"
- **Abbreviations**: "Dr." → "Doctor", "e.g." → "for example"

### Manual Control
- **Edit → Clean Text for TTS**: Apply cleaning to current text
- **Edit → Undo Text Cleaning**: Restore original text
- **Auto-clean on load**: Files automatically processed when opened

## ⚙️ Configuration & Settings

Settings automatically saved to `~/.local-tts-studio/config.json`:
- TTS model preferences
- Audio output quality settings  
- UI customization options
- Default voice cloning settings

## 🚨 Troubleshooting

### Common Issues

**GPU not detected**:
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
```

**Audio device issues (WSL/headless)**:
- Application automatically detects and handles missing audio devices
- Audio generation still works - just save files for playback elsewhere
- Status bar shows "simulating playback" when no audio device available

**Memory issues with large texts**:
```bash
# Reduce chunk size for large documents
python tts_cli.py convert large_book.txt output.wav --chunk-size 1000
```

**Emoji/special characters still appearing**:
- Text is automatically cleaned before synthesis
- Use "Edit → Clean Text for TTS" for manual cleaning
- Check logs for preprocessing details

### Performance Tips
- **GPU recommended**: 5-10x faster than CPU
- **Smaller chunks**: Better for memory-constrained systems  
- **Audio device**: Real playback vs simulation for better experience
- **Voice samples**: 10-30 seconds optimal for cloning quality

## 🔗 What Makes This Interesting

### vs. Other TTS Solutions
- **Truly Offline**: No API keys, no internet required after setup
- **Professional Quality**: XTTS-v2 rivals commercial services
- **Voice Cloning**: Clone any voice from a short sample
- **Smart Processing**: Handles real-world text automatically  
- **Streaming Playback**: Immediate results, not batch processing
- **Production Ready**: Professional architecture and error handling

### Perfect For
- **Content Creators**: Turn scripts into professional narration
- **Accessibility**: Convert documents for audio consumption
- **Language Learning**: Hear text pronunciation in multiple languages
- **Audiobook Creation**: Transform books into professional audiobooks
- **Privacy-Focused**: All processing stays on your machine

## 📄 License

### Application Code
This codebase is licensed under **GPL 3.0** - see LICENSE file for details.

### Model Weights & Third-Party Components
**Important**: This application uses the XTTS-v2 model weights and other third-party libraries, each with their own licensing terms:

- **XTTS-v2 Model Weights**: Licensed under their original terms by Coqui AI. This codebase does not modify, redistribute, or claim any rights over the model weights themselves.
- **Coqui TTS Library**: Licensed under Mozilla Public License 2.0
- **Other Dependencies**: See individual package licenses

**License Clarification**: While this application code is GPL 3.0, we make no claims about changing or affecting the licensing of any model weights, trained models, or third-party libraries used by this application. All third-party components retain their original licensing terms.

## 🙏 Acknowledgments

**Core Technologies**:
- [Coqui TTS](https://github.com/coqui-ai/TTS) - State-of-the-art TTS engine
- [XTTS-v2](https://huggingface.co/coqui/XTTS-v2) - Neural voice cloning model
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - PDF text extraction
- [PyDub](https://github.com/jiaaro/pydub) - Audio processing
