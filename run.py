#!/usr/bin/env python3
"""Main entry point for the Local TTS Studio application."""

import sys
import logging
from pathlib import Path

from src.gui.main_window import MainWindow
from src.config.settings import Settings


def setup_logging():
    """Configure logging for the application."""
    log_dir = Path.home() / ".local-tts-studio" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "local-tts-studio.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Run the application."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Load settings
        config_path = Path.home() / ".local-tts-studio" / "config.json"
        settings = Settings.load_from_file(config_path)
        
        # Create and run GUI
        logger.info("Starting Local TTS Studio")
        app = MainWindow(settings)
        app.run()
        
        # Save settings on exit
        settings.save_to_file(config_path)
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()