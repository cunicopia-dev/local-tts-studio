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
    """Split text into manageable chunks for TTS processing.
    
    Args:
        text: The text to chunk
        max_chars: Maximum characters per chunk
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
        
    # Split by paragraphs first
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    
    for paragraph in paragraphs:
        if len(paragraph) <= max_chars:
            chunks.append(paragraph)
        else:
            # Split long paragraphs by sentences
            sentences = paragraph.replace('. ', '.|').split('|')
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= max_chars:
                    current_chunk += sentence
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
                    
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
    return preprocess_text_with_stats(text)


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