"""
Explanation Engine for generating human-readable explanations
for why text may be flagged as potential fake news.
"""

import re
from utils import split_into_sentences


# Mapping of issue types to human-readable explanations
ISSUE_EXPLANATIONS = {
    'clickbait': "Contains clickbait phrase designed to manipulate readers",
    'emotional_language': "Uses emotionally charged language to provoke reactions",
    'extreme_claims': "Makes extreme or absolute claims without evidence",
    'urgency': "Creates artificial urgency to pressure readers",
    'missing_sources': "Uses vague source attribution instead of credible references",
    'excessive_caps': "Excessive use of capital letters for emphasis",
    'excessive_exclamations': "Overuse of exclamation marks for dramatic effect"
}


# Patterns for sentence-level analysis
SENTENCE_PATTERNS = {
    'medical_claim': {
        'pattern': r'(cure[sd]?|heal[sd]?|treat[sd]?|remedy|miracle).*(disease|cancer|illness|condition|ailment)',
        'reason': "Contains unverified medical claim"
    },
    'conspiracy': {
        'pattern': r'(they|government|media|elites?)\s+(don\'t want|hiding|covering up|won\'t tell)',
        'reason': "Uses conspiracy theory language"
    },
    'absolute_claim': {
        'pattern': r'(100%|always|never|everyone|nobody|all|none)\s+\w+',
        'reason': "Makes absolute claims that are rarely true"
    },
    'fear_mongering': {
        'pattern': r'(warning|danger|threat|deadly|fatal|catastrophic|devastating)',
        'reason': "Uses fear-inducing language"
    },
    'unverified_stat': {
        'pattern': r'\d+%\s+of\s+(people|doctors|scientists|experts)',
        'reason': "Cites statistics without verifiable source"
    },
    'call_to_action': {
        'pattern': r'(share|spread|forward|tell everyone|wake up)',
        'reason': "Urges sharing without fact-checking"
    },
    'sensational': {
        'pattern': r'(shocking|unbelievable|you won\'t believe|mind.?blowing)',
        'reason': "Uses sensationalist language"
    }
}


def analyze_sentence(sentence):
    """
    Analyze a single sentence for fake news indicators.
    
    Args:
        sentence (str): The sentence to analyze
        
    Returns:
        dict or None: Analysis result with sentence and reason, or None if clean
    """
    sentence_lower = sentence.lower()
    
    for pattern_name, pattern_data in SENTENCE_PATTERNS.items():
        if re.search(pattern_data['pattern'], sentence_lower, re.IGNORECASE):
            return {
                'sentence': sentence,
                'reason': pattern_data['reason'],
                'type': pattern_name
            }
    
    # Check for excessive exclamation marks in this sentence
    if sentence.count('!') >= 2:
        return {
            'sentence': sentence,
            'reason': "Multiple exclamation marks suggest sensationalism",
            'type': 'punctuation'
        }
    
    # Check for all-caps words
    words = sentence.split()
    caps_words = [w for w in words if w.isupper() and len(w) > 2]
    if len(caps_words) >= 2:
        return {
            'sentence': sentence,
            'reason': "Excessive capitalization used for emphasis",
            'type': 'caps'
        }
    
    return None


def generate_explanations(text, issues):
    """
    Generate sentence-level explanations for flagged content.
    
    Args:
        text (str): The original text
        issues (list): List of detected issues from NLP analysis
        
    Returns:
        list: List of explanation dictionaries with sentence and reason
    """
    explanations = []
    sentences = split_into_sentences(text)
    
    # Analyze each sentence
    for sentence in sentences:
        result = analyze_sentence(sentence)
        if result:
            explanations.append({
                'sentence': result['sentence'],
                'reason': result['reason']
            })
    
    # If we have issues but no sentence-level explanations, create general ones
    if issues and not explanations:
        for issue in issues:
            issue_type = issue.get('type', '')
            if issue_type in ISSUE_EXPLANATIONS:
                items = issue.get('items', [])
                if items:
                    explanations.append({
                        'sentence': f"Detected: {', '.join(items[:3])}",
                        'reason': ISSUE_EXPLANATIONS[issue_type]
                    })
    
    # Limit to top 5 most relevant explanations
    return explanations[:5]


def create_summary(trust_score, label, explanations):
    """
    Create a summary explanation of the analysis.
    
    Args:
        trust_score (int): The calculated trust score
        label (str): The classification label
        explanations (list): List of explanations
        
    Returns:
        str: Summary text
    """
    if label == "Likely Fake":
        summary = f"This content has a low trust score of {trust_score}/100. "
        summary += "Multiple indicators suggest this may be misinformation. "
    elif label == "Unverified":
        summary = f"This content has a moderate trust score of {trust_score}/100. "
        summary += "Some claims could not be verified and should be fact-checked. "
    else:
        summary = f"This content has a high trust score of {trust_score}/100. "
        summary += "No major red flags were detected, but always verify important claims. "
    
    if explanations:
        summary += f"Found {len(explanations)} potential issue(s) to review."
    
    return summary
