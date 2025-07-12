"""Text processing utilities for handling various text formats."""

from pathlib import Path
from typing import List, Dict, Any
import logging

import fitz  # PyMuPDF
from .text_preprocessing import preprocess_text_for_tts, preprocess_text_with_stats

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text content
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
    try:
        doc = fitz.open(str(pdf_path))
        pages = []
        for page_num, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                pages.append(text)
        doc.close()
        
        return "\n\n".join(pages)
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        raise


def load_text_file(file_path: Path) -> str:
    """Load text from a file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        File content as string
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Text file not found: {file_path}")
        
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Failed to read text file: {e}")
        raise


def chunk_text(text: str, max_chars: int = 2000) -> List[str]:
    """Split text into TTS-appropriate chunks based on tokens, not just characters.
    
    XTTS has a 400 token limit, so we target ~200-250 tokens per chunk for safety.
    Rough estimate: 1 token ≈ 4 characters, so ~800-1000 characters per chunk.
    
    Args:
        text: The text to chunk
        max_chars: Maximum characters per chunk (should be ~800-1000 for XTTS)
        
    Returns:
        List of text chunks
    """
    import re
    
    if not text:
        return []
    
    # Use a very conservative character limit for XTTS token limits
    # XTTS has 400 token limit, aim for ~150 tokens = ~600 characters max
    safe_max_chars = min(max_chars, 600)  # Cap at 600 chars for safety
    
    chunks = []
    
    # First split by double newlines (paragraphs)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    for paragraph in paragraphs:
        if len(paragraph) <= safe_max_chars:
            chunks.append(paragraph)
        else:
            # Split by sentences using proper sentence boundaries
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            
            current_chunk = ""
            for sentence in sentences:
                # Check if adding this sentence would exceed limit
                test_chunk = current_chunk + (" " if current_chunk else "") + sentence
                
                if len(test_chunk) <= safe_max_chars:
                    current_chunk = test_chunk
                else:
                    # Save current chunk and start new one
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
                    
                    # If single sentence is too long, split it further
                    if len(current_chunk) > safe_max_chars:
                        # Split by commas as last resort
                        parts = current_chunk.split(', ')
                        current_chunk = ""
                        for part in parts:
                            test_part = current_chunk + (", " if current_chunk else "") + part
                            if len(test_part) <= safe_max_chars:
                                current_chunk = test_part
                            else:
                                if current_chunk:
                                    chunks.append(current_chunk.strip())
                                current_chunk = part
            
            # Add final chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
    
    return chunks


def estimate_reading_time(text: str, words_per_minute: int = 150) -> float:
    """Estimate reading time in minutes.
    
    Args:
        text: The text to analyze
        words_per_minute: Average speaking rate
        
    Returns:
        Estimated time in minutes
    """
    word_count = len(text.split())
    return word_count / words_per_minute


def load_and_clean_text_file(file_path: Path, auto_clean: bool = True) -> Dict[str, Any]:
    """Load text file and optionally clean it for TTS.
    
    Args:
        file_path: Path to the text file
        auto_clean: Whether to automatically clean the text for TTS
        
    Returns:
        Dictionary with original text, cleaned text, and statistics
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Text file not found: {file_path}")
        
    try:
        original_text = file_path.read_text(encoding='utf-8')
        
        if auto_clean:
            result = preprocess_text_with_stats(original_text)
            logger.info(f"Loaded and cleaned text file: {file_path}")
            return result
        else:
            return {
                'original_text': original_text,
                'processed_text': original_text,
                'statistics': {'processing_steps': ['No cleaning applied']}
            }
    except Exception as e:
        logger.error(f"Failed to read text file: {e}")
        raise


def extract_and_clean_pdf_text(pdf_path: Path, auto_clean: bool = True) -> Dict[str, Any]:
    """Extract text from PDF and optionally clean it for TTS.
    
    Args:
        pdf_path: Path to the PDF file
        auto_clean: Whether to automatically clean the text for TTS
        
    Returns:
        Dictionary with original text, cleaned text, and statistics
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
    try:
        doc = fitz.open(str(pdf_path))
        pages = []
        for page_num, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                pages.append(text)
        doc.close()
        
        original_text = "\n\n".join(pages)
        
        if auto_clean:
            result = preprocess_text_with_stats(original_text)
            logger.info(f"Extracted and cleaned PDF text: {pdf_path}")
            return result
        else:
            return {
                'original_text': original_text,
                'processed_text': original_text,
                'statistics': {'processing_steps': ['No cleaning applied']}
            }
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        raise


def clean_text_for_tts(text: str) -> Dict[str, Any]:
    """Clean existing text for TTS synthesis.
    
    Args:
        text: Text to clean
        
    Returns:
        Dictionary with original text, cleaned text, and statistics
    """
    from src.utils.simple_preprocessing import simple_preprocess_for_tts
    
    processed_text = simple_preprocess_for_tts(text)
    
    return {
        'processed_text': processed_text,
        'statistics': {
            'original_length': len(text),
            'final_length': len(processed_text),
            'length_change': len(processed_text) - len(text),
            'processing_steps': ['Simple preprocessing applied']
        }
    }


def get_cleaning_summary(stats: Dict[str, Any]) -> str:
    """Generate a human-readable summary of text cleaning operations.
    
    Args:
        stats: Statistics from text preprocessing
        
    Returns:
        Human-readable summary string
    """
    if not stats or 'processing_steps' not in stats:
        return "No cleaning performed"
        
    steps = stats['processing_steps']
    if not steps or steps == ['No cleaning applied']:
        return "No cleaning needed"
        
    summary_parts = []
    
    if stats.get('emojis_removed', 0) > 0:
        summary_parts.append(f"Removed {stats['emojis_removed']} emojis")
        
    if stats.get('special_chars_replaced', 0) > 0:
        summary_parts.append(f"Replaced {stats['special_chars_replaced']} special characters")
        
    length_change = stats.get('length_change', 0)
    if length_change != 0:
        change_desc = "reduced" if length_change < 0 else "expanded"
        summary_parts.append(f"Text {change_desc} by {abs(length_change)} characters")
        
    if summary_parts:
        return f"Text cleaned: {', '.join(summary_parts)}"
    else:
        return f"Applied {len(steps)} cleaning steps"