"""
Utility functions for text preprocessing and helper operations.
"""

import re
import string


def clean_text(text):
    """
    Clean and normalize input text.
    
    Args:
        text (str): Raw input text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def split_into_sentences(text):
    """
    Split text into individual sentences.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of sentences
    """
    # Simple sentence splitting using punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def count_exclamation_marks(text):
    """Count exclamation marks in text."""
    return text.count('!')


def count_question_marks(text):
    """Count question marks in text."""
    return text.count('?')


def count_all_caps_words(text):
    """Count words that are entirely in uppercase."""
    words = text.split()
    caps_count = sum(1 for word in words if word.isupper() and len(word) > 1)
    return caps_count


def has_numeric_claims(text):
    """Check if text contains specific numeric claims (percentages, statistics)."""
    patterns = [
        r'\d+%',  # Percentages
        r'\d+\s*(million|billion|thousand)',  # Large numbers
        r'(100%|guaranteed)',  # Absolute claims
    ]
    
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def normalize_score(score, min_val=0, max_val=100):
    """Normalize a score to be within min and max bounds."""
    return max(min_val, min(max_val, score))
