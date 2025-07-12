"""Tests for text processing utilities."""

import unittest
from pathlib import Path
import tempfile

from src.utils.text_processing import chunk_text, load_text_file, estimate_reading_time


class TestTextProcessing(unittest.TestCase):
    """Test text processing functions."""
    
    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        text = "This is a test. " * 100  # ~1600 chars
        chunks = chunk_text(text, max_chars=500)
        
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 500)
            
    def test_chunk_text_paragraphs(self):
        """Test chunking with paragraphs."""
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        chunks = chunk_text(text, max_chars=50)
        
        self.assertEqual(len(chunks), 3)
        
    def test_chunk_empty_text(self):
        """Test chunking empty text."""
        chunks = chunk_text("", max_chars=100)
        self.assertEqual(chunks, [])
        
    def test_load_text_file(self):
        """Test loading text from file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            temp_path = Path(f.name)
            
        try:
            content = load_text_file(temp_path)
            self.assertEqual(content, "Test content")
        finally:
            temp_path.unlink()
            
    def test_estimate_reading_time(self):
        """Test reading time estimation."""
        text = " ".join(["word"] * 150)  # 150 words
        time = estimate_reading_time(text, words_per_minute=150)
        self.assertEqual(time, 1.0)


if __name__ == '__main__':
    unittest.main()