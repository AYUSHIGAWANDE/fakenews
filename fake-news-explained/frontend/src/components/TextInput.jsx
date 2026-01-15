import React from 'react';

/**
 * TextInput Component
 * Large textarea for pasting/typing news with analyze button
 */
function TextInput({ value, onChange, onAnalyze, loading, disabled }) {
    const handleKeyDown = (e) => {
        // Ctrl/Cmd + Enter to analyze
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!disabled && value.trim()) {
                onAnalyze();
            }
        }
    };

    return (
        <div className="input-section">
            <label htmlFor="news-input" className="input-label">
                📰 Paste News Article or Text
            </label>
            <textarea
                id="news-input"
                className="text-input"
                placeholder="Paste the news article, social media post, or any text you want to verify...

Example: 'BREAKING: Scientists discover miracle cure that heals ALL diseases instantly! Share before this gets deleted!'"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
            />
            <button
                className="analyze-btn"
                onClick={onAnalyze}
                disabled={disabled || !value.trim()}
            >
                {loading ? (
                    <>
                        <span className="spinner"></span>
                        Analyzing...
                    </>
                ) : (
                    <>
                        <span className="btn-icon">🔍</span>
                        Analyze News
                    </>
                )}
            </button>
        </div>
    );
}

export default TextInput;
