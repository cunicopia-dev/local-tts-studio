"""Audio utilities for playback and file operations."""

from pathlib import Path
from typing import Optional
import logging
import time
import threading

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play_simpleaudio

logger = logging.getLogger(__name__)


class AudioPlayer:
    """Manages audio playback with stop functionality and device detection."""
    
    def __init__(self):
        self._current_playback = None
        self._simulated_playback = None
        self._has_audio_device = self._check_audio_device()
        
    def _check_audio_device(self) -> bool:
        """Check if an audio device is available."""
        try:
            # Try to play a very short silent audio to test device
            test_audio = AudioSegment.silent(duration=100)  # 100ms silence
            playback = play_simpleaudio(test_audio)
            if playback:
                playback.stop()
                return True
        except Exception as e:
            logger.warning(f"No audio device detected: {e}")
            return False
        return False
        
    def play(self, audio: AudioSegment) -> None:
        """Play an audio segment.
        
        Args:
            audio: The audio to play
        """
        self.stop()  # Stop any current playback
        
        if self._has_audio_device:
            try:
                self._current_playback = play_simpleaudio(audio)
                logger.info("Audio playback started")
                return
            except Exception as e:
                logger.warning(f"Audio device playback failed: {e}")
                # Fall through to simulated playback
                
        # Simulated playback when no audio device is available
        self._simulate_playback(audio)
            
    def _simulate_playback(self, audio: AudioSegment) -> None:
        """Simulate audio playback by waiting for the audio duration."""
        duration = len(audio) / 1000.0  # Convert ms to seconds
        logger.info(f"Simulating audio playback ({duration:.1f}s) - no audio device available")
        
        self._simulated_playback = {
            'start_time': time.time(),
            'duration': duration,
            'stopped': False
        }
        
        def wait_for_duration():
            time.sleep(duration)
            if self._simulated_playback and not self._simulated_playback['stopped']:
                self._simulated_playback = None
                
        thread = threading.Thread(target=wait_for_duration, daemon=True)
        thread.start()
            
    def stop(self) -> None:
        """Stop current playback if any."""
        if self._current_playback:
            try:
                self._current_playback.stop()
                self._current_playback = None
                logger.info("Audio playback stopped")
            except Exception as e:
                logger.error(f"Failed to stop playback: {e}")
                
        if self._simulated_playback:
            self._simulated_playback['stopped'] = True
            self._simulated_playback = None
            logger.info("Simulated audio playback stopped")
                
    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        # Check real playback
        if self._current_playback and self._current_playback.is_playing():
            return True
            
        # Check simulated playback
        if self._simulated_playback:
            elapsed = time.time() - self._simulated_playback['start_time']
            if elapsed < self._simulated_playback['duration'] and not self._simulated_playback['stopped']:
                return True
            else:
                self._simulated_playback = None
                
        return False
        
    def has_audio_device(self) -> bool:
        """Check if an audio device is available."""
        return self._has_audio_device


def save_audio(audio: AudioSegment, output_path: Path, format: str = "wav") -> None:
    """Save audio to file.
    
    Args:
        audio: The audio to save
        output_path: Path where to save the file
        format: Output format (wav or mp3)
    """
    if format not in ["wav", "mp3"]:
        raise ValueError(f"Unsupported format: {format}")
        
    try:
        audio.export(str(output_path), format=format)
        logger.info(f"Audio saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save audio: {e}")
        raise


def load_audio(file_path: Path) -> AudioSegment:
    """Load audio from file.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Loaded AudioSegment
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")
        
    try:
        return AudioSegment.from_file(str(file_path))
    except Exception as e:
        logger.error(f"Failed to load audio: {e}")
        raise