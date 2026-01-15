"""
Core NLP logic for fake news detection.
Contains functions for text analysis and trust score calculation.
"""

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)


# Fake news indicator patterns
CLICKBAIT_PHRASES = [
    "you won't believe",
    "shocking",
    "breaking",
    "this will blow your mind",
    "doctors hate",
    "one weird trick",
    "what happens next",
    "share before",
    "spread this",
    "they don't want you to know",
    "the truth about",
    "secret revealed",
    "must see",
    "going viral",
    "share now",
    "deleted soon",
    "banned",
    "censored",
    "mainstream media won't tell you"
]

EMOTIONAL_WORDS = [
    "outrageous", "unbelievable", "terrifying", "horrifying",
    "devastating", "shocking", "explosive", "bombshell",
    "insane", "crazy", "ridiculous", "disgusting",
    "amazing", "incredible", "miraculous", "stunning"
]

EXTREME_CLAIM_PATTERNS = [
    r"cure[sd]?\s+(all|every|any)",
    r"(100%|completely)\s+(safe|effective|proven)",
    r"(never|always)\s+\w+",
    r"(all|every)\s+\w+\s+(are|is|will)",
    r"(instantly|immediately)\s+(cure|heal|fix|solve)",
    r"(miracle|magic)\s+\w+",
    r"(scientists|doctors|experts)\s+(shocked|amazed|stunned)",
    r"exposed|exposed!",
    r"exposed|exposed!",
]

URGENCY_PATTERNS = [
    r"act now",
    r"limited time",
    r"before it's too late",
    r"hurry",
    r"don't wait",
    r"urgent",
    r"immediately",
    r"right now",
    r"while you still can",
    r"before they delete",
    r"share before"
]

MISSING_SOURCE_INDICATORS = [
    "sources say",
    "people are saying",
    "everyone knows",
    "it is known",
    "many believe",
    "some say",
    "reportedly",
    "allegedly",
    "rumor has it",
    "anonymous sources"
]


def preprocess_text(text):
    """
    Preprocess text for NLP analysis.
    
    Args:
        text (str): Raw input text
        
    Returns:
        dict: Preprocessed text data including tokens and lowercase version
    """
    # Lowercase version
    text_lower = text.lower()
    
    # Tokenize
    try:
        tokens = word_tokenize(text_lower)
    except:
        tokens = text_lower.split()
    
    # Remove stopwords
    try:
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [t for t in tokens if t not in stop_words and t.isalpha()]
    except:
        filtered_tokens = [t for t in tokens if t.isalpha()]
    
    return {
        'original': text,
        'lowercase': text_lower,
        'tokens': tokens,
        'filtered_tokens': filtered_tokens
    }


def detect_clickbait(text_lower):
    """Detect clickbait phrases in text."""
    found = []
    for phrase in CLICKBAIT_PHRASES:
        if phrase in text_lower:
            found.append(phrase)
    return found


def detect_emotional_language(text_lower):
    """Detect emotional and sensational words."""
    found = []
    for word in EMOTIONAL_WORDS:
        if word in text_lower:
            found.append(word)
    return found


def detect_extreme_claims(text):
    """Detect extreme and absolute claims using regex patterns."""
    found = []
    text_lower = text.lower()
    
    for pattern in EXTREME_CLAIM_PATTERNS:
        matches = re.findall(pattern, text_lower)
        if matches:
            found.extend(matches if isinstance(matches[0], str) else [' '.join(m) for m in matches])
    
    return found


def detect_urgency(text_lower):
    """Detect urgency language patterns."""
    found = []
    for pattern in URGENCY_PATTERNS:
        if re.search(pattern, text_lower):
            found.append(pattern)
    return found


def detect_missing_sources(text_lower):
    """Detect vague source attribution."""
    found = []
    for indicator in MISSING_SOURCE_INDICATORS:
        if indicator in text_lower:
            found.append(indicator)
    return found


def count_caps_and_exclamations(text):
    """Count excessive capitalization and punctuation."""
    # Count all-caps words
    words = text.split()
    caps_count = sum(1 for w in words if w.isupper() and len(w) > 2)
    
    # Count exclamation marks
    exclaim_count = text.count('!')
    
    return caps_count, exclaim_count


def calculate_trust_score(text):
    """
    Calculate trust score for the given text.
    
    Args:
        text (str): News text to analyze
        
    Returns:
        dict: Analysis results including score, label, and detected issues
    """
    processed = preprocess_text(text)
    text_lower = processed['lowercase']
    
    # Initialize score at 100 (most trustworthy)
    score = 100
    issues = []
    
    print(f"Initial score: {score}")
    
    # Check for clickbait (-15 points per phrase, max -30)
    clickbait = detect_clickbait(text_lower)
    if clickbait:
        penalty = min(len(clickbait) * 15, 30)
        score -= penalty
        print(f"Clickbait detected: {clickbait}, Penalty: {penalty}, New score: {score}")
        issues.append({
            'type': 'clickbait',
            'items': clickbait,
            'penalty': penalty
        })
    
    # Check for emotional language (-10 points per word, max -25)
    emotional = detect_emotional_language(text_lower)
    if emotional:
        penalty = min(len(emotional) * 10, 25)
        score -= penalty
        print(f"Emotional language detected: {emotional}, Penalty: {penalty}, New score: {score}")
        issues.append({
            'type': 'emotional_language',
            'items': emotional,
            'penalty': penalty
        })
    
    # Check for extreme claims (-20 points per claim, max -40)
    extreme = detect_extreme_claims(text)
    if extreme:
        penalty = min(len(extreme) * 20, 40)
        score -= penalty
        print(f"Extreme claims detected: {extreme}, Penalty: {penalty}, New score: {score}")
        issues.append({
            'type': 'extreme_claims',
            'items': extreme,
            'penalty': penalty
        })
    
    # Check for urgency language (-10 points per pattern, max -20)
    urgency = detect_urgency(text_lower)
    if urgency:
        penalty = min(len(urgency) * 10, 20)
        score -= penalty
        print(f"Urgency detected: {urgency}, Penalty: {penalty}, New score: {score}")
        issues.append({
            'type': 'urgency',
            'items': urgency,
            'penalty': penalty
        })
    
    # Check for missing/vague sources (-15 points per indicator, max -25)
    missing_sources = detect_missing_sources(text_lower)
    if missing_sources:
        penalty = min(len(missing_sources) * 15, 25)
        score -= penalty
        print(f"Missing sources detected: {missing_sources}, Penalty: {penalty}, New score: {score}")
        issues.append({
            'type': 'missing_sources',
            'items': missing_sources,
            'penalty': penalty
        })
    
    # Check for excessive caps and exclamations
    caps_count, exclaim_count = count_caps_and_exclamations(text)
    
    if caps_count > 3:
        penalty = min((caps_count - 3) * 5, 15)
        score -= penalty
        print(f"Excessive caps: {caps_count}, Penalty: {penalty}, New score: {score}")
        issues.append({
            'type': 'excessive_caps',
            'count': caps_count,
            'penalty': penalty
        })
    
    if exclaim_count > 2:
        penalty = min((exclaim_count - 2) * 5, 15)
        score -= penalty
        print(f"Excessive exclamations: {exclaim_count}, Penalty: {penalty}, New score: {score}")
        issues.append({
            'type': 'excessive_exclamations',
            'count': exclaim_count,
            'penalty': penalty
        })
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    print(f"Final score: {score}")
    
    # Determine label
    if score >= 70:
        label = "Likely Real"
    elif score >= 40:
        label = "Unverified"
    else:
        label = "Likely Fake"
    
    return {
        'score': score,
        'label': label,
        'issues': issues
    }
