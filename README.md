# Local TTS Studio

A professional offline text-to-speech studio with voice cloning capabilities. Transform books, documents, and any text into natural-sounding audiobooks using state-of-the-art XTTS-v2 technology.

## Features

- **Multi-format Support**: Load TXT, MD, and PDF files
- **Voice Cloning**: Clone any voice from a WAV sample
- **Chunked Processing**: Efficiently handle large texts
- **Real-time Playback**: Play, pause, and stop controls
- **Export Options**: Save as WAV or MP3
- **Cross-platform**: Works on Windows, macOS, and Linux
- **CLI & GUI**: Both command-line and graphical interfaces

## Installation

### Prerequisites

1. Python 3.8 or higher but not past 3.11
2. FFmpeg (for audio processing)

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/cunicopia-dev/local-tts-studio.git
cd local-tts-studio
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode (Default)

Simply run:
```bash
python run.py
```

Or explicitly:
```bash
python tts_cli.py gui
```

### Command-Line Mode

Convert a text file to audio:
```bash
python tts_cli.py convert input.txt output.wav
```

With voice cloning:
```bash
python tts_cli.py convert book.pdf audiobook.mp3 --voice voice_sample.wav
```

Options:
- `--voice, -v`: WAV file for voice cloning
- `--chunk-size, -c`: Maximum characters per chunk (default: 2000)
- `--gpu`: Enable GPU acceleration
- `--verbose`: Enable detailed logging

### Examples

```bash
# Convert a PDF to MP3 with custom voice
python tts_cli.py convert manual.pdf manual_audio.mp3 --voice john.wav --gpu

# Convert markdown to WAV
python tts_cli.py convert README.md readme_audio.wav

# Process with smaller chunks for better memory usage
python tts_cli.py convert large_book.txt book.mp3 --chunk-size 1000
```

## Project Structure

```
local-tts-studio/
├── src/
│   ├── core/
│   │   └── tts_engine.py      # TTS synthesis engine
│   ├── gui/
│   │   └── main_window.py     # GUI application
│   ├── utils/
│   │   ├── text_processing.py # Text handling utilities
│   │   └── audio_utils.py     # Audio playback/save
│   └── config/
│       └── settings.py        # Configuration management
├── run.py                     # GUI entry point
├── tts_cli.py                # CLI interface
└── requirements.txt          # Python dependencies
```

## Configuration

Settings are stored in `~/.local-tts-studio/config.json` and include:
- TTS model settings
- Audio output preferences
- UI customization options

## Voice Cloning Tips

For best results with voice cloning:
1. Use a clear WAV recording (10-30 seconds)
2. Ensure minimal background noise
3. Include varied speech patterns
4. Sample rate should be 22050 Hz or higher

## Troubleshooting

### GPU Support
If GPU acceleration isn't working:
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
```

### Audio Playback Issues
- Ensure FFmpeg is properly installed
- Check audio device permissions
- Try converting to a different format

### Memory Issues
- Reduce chunk size for large texts
- Use CPU mode if GPU memory is limited
- Process files in smaller sections

## License

[Your License Here]

## Acknowledgments

- Built with [Coqui TTS](https://github.com/coqui-ai/TTS)
- Uses XTTS-v2 model for high-quality synthesis
- PyMuPDF for PDF text extraction