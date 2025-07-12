"""TTS Engine module for handling text-to-speech synthesis."""

import os
import tempfile
from pathlib import Path
from typing import Optional, Callable, List
import logging

from pydub import AudioSegment
from torch.serialization import add_safe_globals
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

# Configure safe globals for PyTorch 2.6+
add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

logger = logging.getLogger(__name__)


class TTSEngine:
    """Manages TTS model initialization and speech synthesis."""
    
    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2", 
                 use_gpu: bool = True):
        """Initialize the TTS engine.
        
        Args:
            model_name: The TTS model to use
            use_gpu: Whether to use GPU acceleration
        """
        self.model_name = model_name
        self.use_gpu = use_gpu
        self._tts: Optional[TTS] = None
        self._speaker_wav: Optional[Path] = None
        
    def initialize(self) -> None:
        """Initialize the TTS model."""
        if self._tts is None:
            logger.info(f"Initializing TTS model: {self.model_name}")
            try:
                self._tts = TTS(
                    model_name=self.model_name,
                    progress_bar=False,
                    gpu=self.use_gpu
                )
                logger.info("TTS model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize TTS model: {e}")
                raise
                
    def set_speaker_voice(self, wav_path: Path) -> None:
        """Set the speaker voice for zero-shot cloning.
        
        Args:
            wav_path: Path to the WAV file for voice cloning
        """
        if not wav_path.exists():
            raise ValueError(f"Speaker WAV file not found: {wav_path}")
        if not wav_path.suffix.lower() == '.wav':
            raise ValueError("Speaker voice must be a WAV file")
        
        self._speaker_wav = wav_path
        logger.info(f"Speaker voice set to: {wav_path}")
        
    def synthesize_chunk(self, text: str, language: str = "en") -> AudioSegment:
        """Synthesize a single text chunk.
        
        Args:
            text: The text to synthesize
            language: Language code (default: "en")
            
        Returns:
            AudioSegment containing the synthesized audio
        """
        if self._tts is None:
            raise RuntimeError("TTS engine not initialized")
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            try:
                # XTTS v2 requires either a speaker_wav or will use a default voice
                if self._speaker_wav:
                    self._tts.tts_to_file(
                        text=text,
                        speaker_wav=str(self._speaker_wav),
                        language=language,
                        file_path=tmp.name,
                    )
                else:
                    # Use predefined speaker (Ana Florence is a default speaker)
                    self._tts.tts_to_file(
                        text=text,
                        speaker="Ana Florence",
                        language=language,
                        file_path=tmp.name,
                    )
                audio = AudioSegment.from_wav(tmp.name)
                return audio
            finally:
                # Clean up temporary file
                if os.path.exists(tmp.name):
                    os.remove(tmp.name)
                    
    def synthesize(self, chunks: List[str], 
                   progress_callback: Optional[Callable[[int, int], None]] = None) -> AudioSegment:
        """Synthesize multiple text chunks into a single audio.
        
        Args:
            chunks: List of text chunks to synthesize
            progress_callback: Optional callback for progress updates (current, total)
            
        Returns:
            Combined AudioSegment
        """
        if not chunks:
            raise ValueError("No text chunks provided")
            
        combined = AudioSegment.silent(duration=0)
        total = len(chunks)
        
        for idx, chunk in enumerate(chunks, 1):
            try:
                audio = self.synthesize_chunk(chunk)
                combined += audio
                
                if progress_callback:
                    progress_callback(idx, total)
                    
            except Exception as e:
                logger.error(f"Failed to synthesize chunk {idx}/{total}: {e}")
                raise
                
        return combined
        
    def synthesize_streaming(self, chunks: List[str], 
                           progress_callback: Optional[Callable[[int, int], None]] = None,
                           audio_callback: Optional[Callable[[AudioSegment], None]] = None) -> AudioSegment:
        """Synthesize multiple text chunks with streaming playback.
        
        Args:
            chunks: List of text chunks to synthesize
            progress_callback: Optional callback for progress updates (current, total)
            audio_callback: Optional callback called with each synthesized audio chunk
            
        Returns:
            Combined AudioSegment
        """
        if not chunks:
            raise ValueError("No text chunks provided")
            
        combined = AudioSegment.silent(duration=0)
        total = len(chunks)
        
        for idx, chunk in enumerate(chunks, 1):
            try:
                # Clean each chunk individually to preserve streaming
                from src.utils.text_preprocessing import preprocess_text_for_tts
                cleaned_chunk = preprocess_text_for_tts(chunk)
                logger.debug(f"Chunk {idx} cleaned: {len(chunk)} -> {len(cleaned_chunk)} chars")
                
                audio = self.synthesize_chunk(cleaned_chunk)
                combined += audio
                
                # Call audio callback for immediate playback
                if audio_callback:
                    audio_callback(audio)
                
                if progress_callback:
                    progress_callback(idx, total)
                    
            except Exception as e:
                logger.error(f"Failed to synthesize chunk {idx}/{total}: {e}")
                raise
                
        return combined