# Fake News Explained 🔍

AI-powered news verification system using Natural Language Processing to detect misinformation and provide transparent explanations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)

## ✨ Features

- **NLP-Based Analysis**: Detects fake news indicators using natural language processing
- **Trust Score**: Calculates a 0-100 credibility score
- **Transparent Explanations**: Provides sentence-level reasoning for flagged content
- **Source Suggestions**: Recommends trusted fact-checking sources
- **Modern UI**: Beautiful glassmorphism design with dark mode

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Flask, NLTK |
| Frontend | React 18, CSS3 |
| API | REST with JSON |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd fake-news-explained/backend

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"

# Start the server
python app.py
```

Backend runs at: `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd fake-news-explained/frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs at: `http://localhost:3000`

## 📡 API Documentation

### POST /analyze

Analyze news text for fake news indicators.

**Request:**
```json
{
  "text": "Your news article text here..."
}
```

**Response:**
```json
{
  "label": "Likely Fake | Unverified | Likely Real",
  "trust_score": 34,
  "explanations": [
    {
      "sentence": "This cures all diseases instantly!",
      "reason": "Extreme medical claim without evidence"
    }
  ],
  "sources": ["Reuters", "FactCheck.org", "BBC News"],
  "summary": "Analysis summary text..."
}
```

### GET /health

Health check endpoint.

## 🎯 How It Works

1. **Text Preprocessing**: Cleans and tokenizes input text
2. **Indicator Detection**: Identifies:
   - Clickbait phrases
   - Emotional language
   - Extreme claims
   - Urgency patterns
   - Vague source attribution
3. **Score Calculation**: Computes trust score based on detected issues
4. **Explanation Generation**: Creates human-readable explanations
5. **Source Recommendation**: Suggests relevant fact-checking sources

## 🎨 Screenshots

The application features a modern dark theme with:
- Glassmorphism card effects
- Color-coded result badges (🔴🟡🟢)
- Animated trust score progress bar
- Expandable explanation panels
- Clickable verification sources

## 🔮 Future Enhancements

- [ ] Machine Learning model integration
- [ ] Multilingual support
- [ ] Browser extension
- [ ] API rate limiting
- [ ] User authentication
- [ ] History tracking

## ⚠️ Disclaimer

> **This system assists news verification and does not replace professional fact-checking.**
> 
> The analysis is based on linguistic patterns and heuristics. Always verify important information with multiple trusted sources. This tool should be used as one of many resources in evaluating news credibility.

## 📄 License

MIT License - feel free to use and modify for your projects.

---

Built with ❤️ using NLP and React
