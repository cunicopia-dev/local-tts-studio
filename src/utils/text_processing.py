"""Text processing utilities for handling various text formats."""

from pathlib import Path
from typing import List
import logging

import fitz  # PyMuPDF

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