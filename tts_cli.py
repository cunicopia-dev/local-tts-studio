#!/usr/bin/env python3
"""Command-line interface for TTS operations."""

import argparse
import sys
import logging
from pathlib import Path

from src.core.tts_engine import TTSEngine
from src.utils.text_processing import load_text_file, extract_text_from_pdf, chunk_text
from src.utils.audio_utils import save_audio
from src.config.settings import Settings


def setup_cli_logging(verbose: bool = False):
    """Setup logging for CLI mode."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def process_file(args):
    """Process a text file to audio."""
    logger = logging.getLogger(__name__)
    
    # Load settings
    settings = Settings.load_defaults()
    
    # Initialize TTS engine
    logger.info("Initializing TTS engine...")
    engine = TTSEngine(use_gpu=args.gpu)
    engine.initialize()
    
    # Set voice if provided
    if args.voice:
        voice_path = Path(args.voice)
        logger.info(f"Loading voice sample: {voice_path}")
        engine.set_speaker_voice(voice_path)
    
    # Load text
    input_path = Path(args.input)
    logger.info(f"Loading text from: {input_path}")
    
    if input_path.suffix.lower() == '.pdf':
        text = extract_text_from_pdf(input_path)
    else:
        text = load_text_file(input_path)
    
    # Process text
    chunks = chunk_text(text, args.chunk_size)
    logger.info(f"Processing {len(chunks)} text chunks...")
    
    def progress_callback(current, total):
        print(f"\rProgress: {current}/{total} chunks", end='', flush=True)
    
    audio = engine.synthesize(chunks, progress_callback)
    print()  # New line after progress
    
    # Save output
    output_path = Path(args.output)
    format = "mp3" if output_path.suffix.lower() == '.mp3' else "wav"
    logger.info(f"Saving audio to: {output_path}")
    save_audio(audio, output_path, format)
    
    logger.info("Processing complete!")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Local TTS Studio - Convert text to speech"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert text to audio')
    convert_parser.add_argument('input', help='Input text/PDF file')
    convert_parser.add_argument('output', help='Output audio file (WAV/MP3)')
    convert_parser.add_argument(
        '--voice', '-v', 
        help='WAV file for voice cloning'
    )
    convert_parser.add_argument(
        '--chunk-size', '-c', 
        type=int, 
        default=2000,
        help='Maximum characters per chunk (default: 2000)'
    )
    convert_parser.add_argument(
        '--gpu', 
        action='store_true',
        help='Use GPU acceleration'
    )
    convert_parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    # GUI command (default)
    gui_parser = subparsers.add_parser('gui', help='Launch GUI application')
    
    args = parser.parse_args()
    
    # Default to GUI if no command specified
    if args.command is None:
        args.command = 'gui'
    
    if args.command == 'convert':
        setup_cli_logging(args.verbose)
        try:
            process_file(args)
        except Exception as e:
            logging.error(f"Error: {e}")
            sys.exit(1)
    elif args.command == 'gui':
        from run import main as run_gui
        run_gui()


if __name__ == "__main__":
    main()