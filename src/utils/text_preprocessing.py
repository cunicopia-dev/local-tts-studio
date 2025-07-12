"""Advanced text preprocessing for TTS optimization."""

import re
import unicodedata
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class TTSTextPreprocessor:
    """Intelligent text preprocessing for optimal TTS synthesis."""
    
    def __init__(self):
        self.emoji_patterns = self._build_emoji_patterns()
        self.replacements = self._build_replacement_dict()
        
    def _build_emoji_patterns(self) -> re.Pattern:
        """Build comprehensive regex pattern to match ALL emojis and symbols."""
        # Comprehensive Unicode ranges for emojis and symbols
        emoji_pattern = re.compile(
            "["
            # Core emoji blocks
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Misc Symbols and Pictographs
            "\U0001F680-\U0001F6FF"  # Transport and Map Symbols
            "\U0001F700-\U0001F77F"  # Alchemical Symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002600-\U000026FF"  # Miscellaneous Symbols
            "\U00002700-\U000027BF"  # Dingbats
            "\U0001F1E0-\U0001F1FF"  # Regional Indicator Symbols (flags)
            
            # Extended ranges for newer emojis
            "\U0001F004\U0001F0CF"   # Mahjong tile, Playing card
            "\U0001F170-\U0001F251"  # Enclosed characters
            "\U0001F910-\U0001F96B"  # Additional emoticons
            "\U0001F980-\U0001F997"  # Additional symbols
            "\U0001F9C0-\U0001F9FF"  # More symbols
            
            # Mathematical and technical symbols
            "\U00002000-\U0000206F"  # General Punctuation
            "\U00002070-\U0000209F"  # Superscripts and Subscripts
            "\U000020A0-\U000020CF"  # Currency Symbols
            "\U000020D0-\U000020FF"  # Combining Diacritical Marks for Symbols
            "\U00002100-\U0000214F"  # Letterlike Symbols
            "\U00002150-\U0000218F"  # Number Forms
            "\U00002190-\U000021FF"  # Arrows
            "\U00002200-\U000022FF"  # Mathematical Operators
            "\U00002300-\U000023FF"  # Miscellaneous Technical
            "\U00002400-\U0000243F"  # Control Pictures
            "\U00002440-\U0000245F"  # Optical Character Recognition
            "\U00002460-\U000024FF"  # Enclosed Alphanumerics
            "\U00002500-\U0000257F"  # Box Drawing
            "\U00002580-\U0000259F"  # Block Elements
            "\U000025A0-\U000025FF"  # Geometric Shapes
            "\U00002600-\U000026FF"  # Miscellaneous Symbols (repeated for completeness)
            "\U00002700-\U000027BF"  # Dingbats (repeated for completeness)
            
            # Additional symbol ranges
            "\U0000FE00-\U0000FE0F"  # Variation Selectors
            "\U0000FE20-\U0000FE2F"  # Combining Half Marks
            "\U00003000-\U0000303F"  # CJK Symbols and Punctuation
            "\U00003200-\U000032FF"  # Enclosed CJK Letters and Months
            "\U00003300-\U000033FF"  # CJK Compatibility
            
            # Special characters that often appear as emojis
            "\u200d"                 # Zero Width Joiner
            "\ufe0f"                 # Variation Selector-16
            "\u20e3"                 # Combining Enclosing Keycap
            "]+"
        )
        return emoji_pattern
        
    def _build_replacement_dict(self) -> Dict[str, str]:
        """Build dictionary of problematic characters and their TTS-friendly replacements."""
        return {
            # Common problematic characters
            '"': '"',           # Smart quotes to regular quotes
            '"': '"',
            ''': "'",           # Smart apostrophes to regular apostrophes
            ''': "'",
            '`': "'",           # Grave accent to regular apostrophe
            '´': "'",           # Acute accent to regular apostrophe
            '–': '-',           # En dash to hyphen
            '—': ' - ',         # Em dash to spaced hyphen
            '…': '...',         # Ellipsis to three dots
            '®': ' registered trademark ',
            '™': ' trademark ',
            '©': ' copyright ',
            '°': ' degrees ',
            '€': ' euros ',
            '£': ' pounds ',
            '¥': ' yen ',
            '$': ' dollars ',
            '&': ' and ',
            '@': ' at ',
            '#': ' number ',
            '%': ' percent ',
            
            # Mathematical symbols
            '×': ' times ',
            '÷': ' divided by ',
            '±': ' plus or minus ',
            '²': ' squared ',
            '³': ' cubed ',
            '½': ' one half ',
            '¼': ' one quarter ',
            '¾': ' three quarters ',
            
            # Common abbreviations that should be spoken
            'e.g.': 'for example',
            'i.e.': 'that is',
            'etc.': 'etcetera',
            'vs.': 'versus',
            'Mr.': 'Mister',
            'Mrs.': 'Missus', 
            'Ms.': 'Miss',
            'Dr.': 'Doctor',
            'Prof.': 'Professor',
            'Inc.': 'Incorporated',
            'Ltd.': 'Limited',
            'Corp.': 'Corporation',
            'Co.': 'Company',
            
            # Internet/tech terms
            'URL': 'U R L',
            'HTTP': 'H T T P',
            'HTML': 'H T M L',
            'CSS': 'C S S',
            'JS': 'JavaScript',
            'API': 'A P I',
            'UI': 'U I',
            'UX': 'U X',
        }
        
    def normalize_line_endings(self, text: str) -> str:
        """Normalize line endings and convert to speech-friendly pauses."""
        # Convert CRLF and CR to LF first
        text = text.replace('\r\n', '\n')  # Windows CRLF
        text = text.replace('\r', '\n')    # Old Mac CR
        
        # Convert paragraph breaks (double newlines) to periods for better TTS pacing
        text = text.replace('\n\n', '. ')  # Paragraph breaks become periods
        
        # Convert single newlines to brief pauses (spaces) for better flow
        text = text.replace('\n', ' ')  # Single newlines become spaces
        
        return text
        
    def remove_emojis(self, text: str, replace_with: str = " ") -> Tuple[str, int]:
        """Remove emojis from text.
        
        Args:
            text: Input text
            replace_with: What to replace emojis with (default: space)
            
        Returns:
            Tuple of (cleaned_text, emoji_count)
        """
        original_length = len(text)
        cleaned = self.emoji_patterns.sub(replace_with, text)
        
        # Fix emoji count calculation - count actual matches, not spaces
        matches = list(self.emoji_patterns.finditer(text))
        emoji_count = len(matches)
        
        # Clean up multiple spaces but preserve newlines
        cleaned = re.sub(r'[ \t]+', ' ', cleaned).strip()
        
        return cleaned, emoji_count
        
    def replace_special_characters(self, text: str) -> Tuple[str, int]:
        """Replace special characters with TTS-friendly alternatives.
        
        Returns:
            Tuple of (processed_text, replacement_count)
        """
        processed = text
        replacement_count = 0
        
        for original, replacement in self.replacements.items():
            if original in processed:
                count = processed.count(original)
                processed = processed.replace(original, replacement)
                replacement_count += count
                
        return processed, replacement_count
        
    def normalize_unicode(self, text: str) -> str:
        """Normalize Unicode characters to standard forms while preserving essential punctuation."""
        # Normalize to NFD (decomposed) then to NFC (composed)
        normalized = unicodedata.normalize('NFD', text)
        normalized = unicodedata.normalize('NFC', normalized)
        
        # Remove only control characters, but preserve all punctuation including apostrophes
        normalized = ''.join(
            char for char in normalized 
            if not (unicodedata.category(char).startswith('C') and char not in '\n\t')
        )
        
        return normalized
        
    def clean_whitespace(self, text: str) -> str:
        """Clean up excessive whitespace while preserving paragraph structure."""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple newlines with max 2 (paragraph break)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Remove leading/trailing whitespace from lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
        
    def handle_urls_and_emails(self, text: str) -> str:
        """Replace URLs and email addresses with speakable text."""
        # Replace URLs
        url_pattern = re.compile(
            r'https?://[^\s<>"{}|\\^`\[\]]+',
            re.IGNORECASE
        )
        text = url_pattern.sub(' web link ', text)
        
        # Replace email addresses
        email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        text = email_pattern.sub(' email address ', text)
        
        return text
        
    def handle_numbers_and_dates(self, text: str) -> str:
        """Improve number and date pronunciation."""
        # Handle years (4 digits)
        text = re.sub(r'\b(19|20)\d{2}\b', lambda m: f" {m.group()} ", text)
        
        # Handle phone numbers (basic pattern)
        phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
        text = phone_pattern.sub(' phone number ', text)
        
        # Handle large numbers with commas
        text = re.sub(r'\b\d{1,3}(,\d{3})+\b', lambda m: m.group().replace(',', ' '), text)
        
        return text
        
    def preprocess_for_tts(self, text: str, 
                          remove_emojis: bool = True,
                          replace_special_chars: bool = True,
                          normalize_unicode: bool = True,
                          clean_urls_emails: bool = True,
                          improve_numbers: bool = True) -> Dict[str, any]:
        """Complete preprocessing pipeline for TTS optimization.
        
        Args:
            text: Input text to process
            remove_emojis: Whether to remove emoji characters
            replace_special_chars: Whether to replace special characters
            normalize_unicode: Whether to normalize Unicode
            clean_urls_emails: Whether to handle URLs and emails
            improve_numbers: Whether to improve number pronunciation
            
        Returns:
            Dictionary with processed text and statistics
        """
        original_text = text
        stats = {
            'original_length': len(text),
            'emojis_removed': 0,
            'special_chars_replaced': 0,
            'processing_steps': []
        }
        
        # Step 1: Normalize line endings
        text = self.normalize_line_endings(text)
        stats['processing_steps'].append('Line endings normalized')
        
        # Step 2: Unicode normalization
        if normalize_unicode:
            text = self.normalize_unicode(text)
            stats['processing_steps'].append('Unicode normalized')
            
        # Step 3: Remove emojis
        if remove_emojis:
            text, emoji_count = self.remove_emojis(text)
            stats['emojis_removed'] = emoji_count
            if emoji_count > 0:
                stats['processing_steps'].append(f'Removed {emoji_count} emojis')
                
        # Step 4: Replace special characters
        if replace_special_chars:
            text, replacement_count = self.replace_special_characters(text)
            stats['special_chars_replaced'] = replacement_count
            if replacement_count > 0:
                stats['processing_steps'].append(f'Replaced {replacement_count} special characters')
                
        # Step 5: Handle URLs and emails
        if clean_urls_emails:
            text = self.handle_urls_and_emails(text)
            stats['processing_steps'].append('URLs and emails processed')
            
        # Step 6: Improve numbers and dates
        if improve_numbers:
            text = self.handle_numbers_and_dates(text)
            stats['processing_steps'].append('Numbers and dates improved')
            
        # Step 7: Clean whitespace
        text = self.clean_whitespace(text)
        stats['processing_steps'].append('Whitespace cleaned')
        
        stats['final_length'] = len(text)
        stats['length_change'] = stats['final_length'] - stats['original_length']
        
        logger.info(f"Text preprocessing complete: {len(stats['processing_steps'])} steps applied")
        
        return {
            'original_text': original_text,
            'processed_text': text,
            'statistics': stats
        }


# Global preprocessor instance
_preprocessor = TTSTextPreprocessor()

def preprocess_text_for_tts(text: str, **kwargs) -> str:
    """Convenience function for text preprocessing."""
    result = _preprocessor.preprocess_for_tts(text, **kwargs)
    return result['processed_text']

def preprocess_text_with_stats(text: str, **kwargs) -> Dict[str, any]:
    """Convenience function for text preprocessing with detailed statistics."""
    return _preprocessor.preprocess_for_tts(text, **kwargs)