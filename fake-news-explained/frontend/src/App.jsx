import React, { useState } from 'react';
import { analyzeNews } from './api';
import TextInput from './components/TextInput';
import ResultBadge from './components/ResultBadge';
import TrustScore from './components/TrustScore';
import ExplanationBox from './components/ExplanationBox';
import SourceLinks from './components/SourceLinks';

/**
 * Main App Component
 * Fake News Explained - NLP-Based News Verification System
 */
function App() {
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

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

    return (
        <div className="app">
            {/* Header */}
            <header className="header">
                <div className="logo">
                    <span className="logo-icon">🔍</span>
                    <h1 className="title">Fake News Explained</h1>
                </div>
                <p className="subtitle">
                    AI-powered news verification using Natural Language Processing
                </p>
            </header>

            {/* Main Content */}
            <main>
                <div className="glass-card">
                    {/* Text Input */}
                    <TextInput
                        value={text}
                        onChange={setText}
                        onAnalyze={handleAnalyze}
                        loading={loading}
                        disabled={loading}
                    />

                    {/* Error State */}
                    {error && (
                        <div className="error-box">
                            <p>❌ {error}</p>
                        </div>
                    )}

                    {/* Results Section */}
                    {result && (
                        <div className="results-section">
                            {/* Result Badge */}
                            <ResultBadge label={result.label} />

                            {/* Trust Score */}
                            <TrustScore score={result.trust_score} label={result.label} />

                            {/* Summary */}
                            {result.summary && (
                                <div className="summary-box">
                                    {result.summary}
                                </div>
                            )}

                            {/* Explanations */}
                            <ExplanationBox explanations={result.explanations} />

                            {/* Source Links */}
                            <SourceLinks sources={result.sources} />
                        </div>
                    )}

                    {/* Empty State */}
                    {!result && !loading && !error && (
                        <div className="empty-state">
                            <div className="empty-icon">📋</div>
                            <p>Paste or type news content above and click "Analyze News" to check its credibility.</p>
                        </div>
                    )}
                </div>

                {/* Disclaimer */}
                <div className="disclaimer">
                    <span className="disclaimer-icon">⚠️</span>
                    This system assists news verification and does not replace professional fact-checking.
                    Always verify important information with multiple trusted sources.
                </div>
            </main>
        </div>
    );
}

export default App;
