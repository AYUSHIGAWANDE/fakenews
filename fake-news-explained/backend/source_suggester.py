"""
Source Suggester module for recommending trusted fact-checking
and verification sources based on content type.
"""

# Trusted fact-checking sources
FACT_CHECK_SOURCES = [
    {
        'name': 'FactCheck.org',
        'url': 'https://www.factcheck.org',
        'description': 'Nonpartisan fact-checking from the Annenberg Public Policy Center'
    },
    {
        'name': 'Snopes',
        'url': 'https://www.snopes.com',
        'description': 'Oldest and largest fact-checking site online'
    },
    {
        'name': 'PolitiFact',
        'url': 'https://www.politifact.com',
        'description': 'Pulitzer Prize-winning political fact-checking'
    }
]

# Trusted news sources
NEWS_SOURCES = [
    {
        'name': 'Reuters',
        'url': 'https://www.reuters.com',
        'description': 'International news organization known for unbiased reporting'
    },
    {
        'name': 'Associated Press',
        'url': 'https://apnews.com',
        'description': 'Nonprofit news agency with global coverage'
    },
    {
        'name': 'BBC News',
        'url': 'https://www.bbc.com/news',
        'description': 'British public service broadcaster'
    }
]

# Medical/health verification sources
HEALTH_SOURCES = [
    {
        'name': 'WHO',
        'url': 'https://www.who.int',
        'description': 'World Health Organization official information'
    },
    {
        'name': 'CDC',
        'url': 'https://www.cdc.gov',
        'description': 'Centers for Disease Control and Prevention'
    },
    {
        'name': 'NIH',
        'url': 'https://www.nih.gov',
        'description': 'National Institutes of Health'
    }
]

# Science verification sources
SCIENCE_SOURCES = [
    {
        'name': 'Nature',
        'url': 'https://www.nature.com',
        'description': 'Leading international scientific journal'
    },
    {
        'name': 'Science Magazine',
        'url': 'https://www.science.org',
        'description': 'Peer-reviewed academic journal by AAAS'
    }
]

# Keywords for content categorization
HEALTH_KEYWORDS = ['cure', 'disease', 'vaccine', 'medicine', 'doctor', 'health', 
                   'hospital', 'treatment', 'symptom', 'virus', 'cancer', 'covid']

SCIENCE_KEYWORDS = ['research', 'study', 'scientist', 'discovery', 'experiment',
                    'laboratory', 'evidence', 'data', 'climate', 'space', 'physics']

POLITICAL_KEYWORDS = ['election', 'politician', 'government', 'congress', 'senate',
                      'president', 'vote', 'campaign', 'policy', 'law', 'democrat',
                      'republican', 'liberal', 'conservative']


def categorize_content(text):
    """
    Categorize content based on keywords.
    
    Args:
        text (str): The news text
        
    Returns:
        set: Set of content categories
    """
    text_lower = text.lower()
    categories = set()
    
    for keyword in HEALTH_KEYWORDS:
        if keyword in text_lower:
            categories.add('health')
            break
    
    for keyword in SCIENCE_KEYWORDS:
        if keyword in text_lower:
            categories.add('science')
            break
    
    for keyword in POLITICAL_KEYWORDS:
        if keyword in text_lower:
            categories.add('political')
            break
    
    return categories


def get_suggested_sources(text, label):
    """
    Get suggested verification sources based on content and classification.
    
    Args:
        text (str): The analyzed text
        label (str): The classification label (Likely Fake, Unverified, Likely Real)
        
    Returns:
        list: List of source dictionaries with name, url, and description
    """
    sources = []
    categories = categorize_content(text)
    
    # Always include top fact-checkers for dubious content
    if label in ["Likely Fake", "Unverified"]:
        sources.extend(FACT_CHECK_SOURCES[:2])  # Add top 2 fact-checkers
    
    # Add category-specific sources
    if 'health' in categories:
        sources.extend(HEALTH_SOURCES[:2])
    
    if 'science' in categories:
        sources.extend(SCIENCE_SOURCES[:1])
    
    if 'political' in categories:
        sources.append(FACT_CHECK_SOURCES[2])  # PolitiFact
    
    # Always include at least one major news source
    sources.extend(NEWS_SOURCES[:2])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_sources = []
    for source in sources:
        if source['name'] not in seen:
            seen.add(source['name'])
            unique_sources.append(source)
    
    # Return top 5 sources
    return unique_sources[:5]


def get_source_names(sources):
    """
    Extract just the names from source list.
    
    Args:
        sources (list): List of source dictionaries
        
    Returns:
        list: List of source names
    """
    return [s['name'] for s in sources]
