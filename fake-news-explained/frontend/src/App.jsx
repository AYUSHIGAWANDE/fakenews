import React, { useState, useRef } from 'react';
import { analyzeNews } from './api';
import TextInput from './components/TextInput';
import ResultBadge from './components/ResultBadge';
import TrustScore from './components/TrustScore';
import ExplanationBox from './components/ExplanationBox';
import SourceLinks from './components/SourceLinks';

/**
 * VerifiNews - AI-Powered News Verification
 */
function App() {
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const toolRef = useRef(null);

    const handleAnalyze = async () => {
        if (!text.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await analyzeNews(text);
            setResult(data);
        } catch (err) {
            setError(err.message || 'An error occurred while analyzing the text.');
        } finally {
            setLoading(false);
        }
    };

    const scrollToTool = () => {
        toolRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const ShieldIcon = ({ className }) => (
        <svg className={className} width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M9 12L11 14L15 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
    );

    return (
        <div className="app-container">
            {/* Navbar */}
            <nav className="navbar">
                <a href="/" className="brand">
                    <div className="brand-logo">
                        <ShieldIcon className="text-white" />
                    </div>
                    <span className="brand-name">VerifiNews</span>
                </a>
                <div className="nav-links">
                    <a href="#" className="nav-link active">Home</a>
                    <a href="#" onClick={scrollToTool} className="nav-link">Detect</a>
                    <a href="#" className="nav-link">About</a>
                </div>
            </nav>

            {/* Hero Section */}
            <header className="hero fade-in">
                <div className="hero-shield">
                    <ShieldIcon className="text-secondary" />
                </div>
                <h1 className="hero-title">
                    Detect Fake News Instantly <br /> with AI
                </h1>
                <p className="hero-subtitle">
                    An intelligent system that analyzes news credibility in seconds using
                    advanced machine learning and natural language processing.
                </p>
                <button className="cta-button" onClick={scrollToTool}>
                    <span className="sparkle-icon">✨</span>
                    Start Detection
                </button>
            </header>

            {/* Main Content / Tool Section */}
            <main ref={toolRef} className="tool-section fade-in" style={{ animationDelay: '0.2s' }}>
                <div className="glass-card">
                    <TextInput
                        value={text}
                        onChange={setText}
                        onAnalyze={handleAnalyze}
                        loading={loading}
                        disabled={loading}
                    />

                    {/* Error State */}
                    {error && (
                        <div className="error-box" style={{ marginTop: '20px' }}>
                            <p>❌ {error}</p>
                        </div>
                    )}

                    {/* Results Section */}
                    {result && (
                        <div className="results-container fade-in">
                            <div style={{ display: 'flex', justifyContent: 'center' }}>
                                <ResultBadge label={result.label} />
                            </div>

                            <TrustScore score={result.trust_score} label={result.label} />

                            {result.summary && (
                                <div className="summary-box">
                                    <h4 className="summary-title">AI Summary</h4>
                                    <p className="summary-text">{result.summary}</p>
                                </div>
                            )}

                            <div style={{ marginTop: '32px' }}>
                                <ExplanationBox explanations={result.explanations} />
                            </div>

                            <div style={{ marginTop: '32px' }}>
                                <SourceLinks sources={result.sources} />
                            </div>
                        </div>
                    )}
                </div>

                <p className="disclaimer-text">
                    Disclaimer: This tool uses AI to assist in verification and should not be used as the sole source for truth.
                    Always verify information with trusted secondary sources.
                </p>
            </main>

            {/* Footer space */}
            <div style={{ height: '100px' }}></div>
        </div>
    );
}

export default App;
