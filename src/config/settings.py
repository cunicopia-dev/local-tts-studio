"""Configuration settings for the TTS application."""

from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class TTSConfig:
    """TTS engine configuration."""
    model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    use_gpu: bool = True
    chunk_size: int = 200  # Very conservative limit for XTTS 250-character warning
    

@dataclass
class AudioConfig:
    """Audio processing configuration."""
    output_format: str = "wav"
    sample_rate: int = 22050
    

@dataclass
class AppConfig:
    """Application configuration."""
    window_width: int = 720
    window_height: int = 520
    font_family: str = "Arial"
    font_size: int = 11
    theme: str = "default"
    

@dataclass
class Settings:
    """Application settings container."""
    tts: TTSConfig
    audio: AudioConfig
    app: AppConfig
    
    @classmethod
    def load_defaults(cls) -> 'Settings':
        """Load default settings."""
        return cls(
            tts=TTSConfig(),
            audio=AudioConfig(),
            app=AppConfig()
        )
        
    @classmethod
    def load_from_file(cls, config_path: Path) -> 'Settings':
        """Load settings from JSON file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Settings instance
        """
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return cls.load_defaults()
            
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                
            return cls(
                tts=TTSConfig(**data.get('tts', {})),
                audio=AudioConfig(**data.get('audio', {})),
                app=AppConfig(**data.get('app', {}))
            )
        except Exception as e:
            logger.error(f"Failed to load config: {e}, using defaults")
            return cls.load_defaults()
            
    def save_to_file(self, config_path: Path) -> None:
        """Save settings to JSON file.
        
        Args:
            config_path: Path where to save configuration
        """
        try:
            data = {
                'tts': {
                    'model_name': self.tts.model_name,
                    'use_gpu': self.tts.use_gpu,
                    'chunk_size': self.tts.chunk_size
                },
                'audio': {
                    'output_format': self.audio.output_format,
                    'sample_rate': self.audio.sample_rate
                },
                'app': {
                    'window_width': self.app.window_width,
                    'window_height': self.app.window_height,
                    'font_family': self.app.font_family,
                    'font_size': self.app.font_size,
                    'theme': self.app.theme
                }
            }
            
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Settings saved to: {config_path}")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            raise