#!/usr/bin/env python3
"""Simple, minimal text preprocessing for TTS."""

import re
import unicodedata


def simple_preprocess_for_tts(text: str) -> str:
    """Minimal preprocessing - only keep characters good for TTS.
    
    NOTE: This is called AFTER chunking, so we only process individual chunks.
    
    Args:
        text: Input text chunk
        
    Returns:
        Cleaned text with only TTS-friendly characters
    """
    if not text:
        return ""
    
    # Step 1: Convert line breaks to speech pauses (for chunks)
    # Since this runs on individual chunks, just convert remaining newlines to periods
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = text.replace('\n', '. ')    # Any remaining newlines become periods
    
    # Step 2: Normalize Windows smart quotes to regular punctuation FIRST
    # Use explicit Unicode code points to avoid any confusion
    text = text.replace(chr(0x2019), "'")    # U+2019 RIGHT SINGLE QUOTATION MARK → apostrophe
    text = text.replace(chr(0x2018), "'")    # U+2018 LEFT SINGLE QUOTATION MARK → apostrophe  
    text = text.replace(chr(0x201C), '"')    # U+201C LEFT DOUBLE QUOTATION MARK → quote
    text = text.replace(chr(0x201D), '"')    # U+201D RIGHT DOUBLE QUOTATION MARK → quote
    text = text.replace(chr(0x2014), '-')    # U+2014 EM DASH → hyphen
    text = text.replace(chr(0x2013), '-')    # U+2013 EN DASH → hyphen
    
    # Step 3: Keep only basic TTS-friendly characters
    allowed_chars = set(
        'abcdefghijklmnopqrstuvwxyz'      # lowercase letters
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'      # uppercase letters  
        '0123456789'                      # numbers
        ' .,!?;:-()[]"\''                 # basic punctuation including apostrophe
        '\t'                              # tab
    )
    
    # Step 4: Remove emojis and unwanted characters (replace with space)
    filtered_chars = []
    for char in text:
        if char in allowed_chars:
            filtered_chars.append(char)
        else:
            # Replace any unwanted character (emojis, etc.) with space
            filtered_chars.append(' ')
    
    text = ''.join(filtered_chars)
    
    # Step 5: Clean up excessive whitespace
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
    text = text.strip()
    
    return text


def preprocess_text_for_tts(text: str) -> str:
    """Main preprocessing function - just calls simple version."""
    return simple_preprocess_for_tts(text)