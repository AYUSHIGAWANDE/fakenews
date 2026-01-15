"""
Fake News Explained - Flask REST API
Main application entry point for the fake news detection service.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from utils import clean_text
from nlp_logic import calculate_trust_score
from explanation_engine import generate_explanations, create_summary
from source_suggester import get_suggested_sources, get_source_names

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint."""
    return jsonify({
        'status': 'online',
        'message': 'Fake News Explained API is running',
        'version': '1.0.0'
    })


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze news text for fake news indicators.
    
    Expected JSON body:
    {
        "text": "The news article text to analyze..."
    }
    
    Returns:
    {
        "label": "Likely Fake | Unverified | Likely Real",
        "trust_score": 0-100,
        "explanations": [{"sentence": "...", "reason": "..."}],
        "sources": ["Source Name", ...],
        "sources_detailed": [{"name": "...", "url": "...", "description": "..."}],
        "summary": "Brief summary of analysis"
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text',
                'message': 'Please provide news text to analyze'
            }), 400
        
        text = data['text']
        
        # Validate text
        if not text or not text.strip():
            return jsonify({
                'error': 'Empty text provided',
                'message': 'Please provide non-empty news text to analyze'
            }), 400
        
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Calculate trust score and get issues
        analysis = calculate_trust_score(cleaned_text)
        trust_score = analysis['score']
        label = analysis['label']
        issues = analysis['issues']
        
        # Generate explanations
        explanations = generate_explanations(cleaned_text, issues)
        
        # Get suggested sources
        sources_detailed = get_suggested_sources(cleaned_text, label)
        sources = get_source_names(sources_detailed)
        
        # Create summary
        summary = create_summary(trust_score, label, explanations)
        
        # Return analysis results
        return jsonify({
            'label': label,
            'trust_score': trust_score,
            'explanations': explanations,
            'sources': sources,
            'sources_detailed': sources_detailed,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for monitoring."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    print("Starting Fake News Explained API...")
    print("API running at: http://localhost:5000")
    print("POST /analyze - Analyze news text")
    print("GET /health - Health check")
    app.run(host='0.0.0.0', port=5000, debug=True)
