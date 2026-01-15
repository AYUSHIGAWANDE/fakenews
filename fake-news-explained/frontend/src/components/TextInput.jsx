import React from 'react';

/**
 * TextInput Component
 * Premium textarea for news content
 */
function TextInput({ value, onChange, onAnalyze, loading, disabled }) {
    const handleKeyDown = (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!disabled && value.trim()) {
                onAnalyze();
            }
        }
    };

    return (
        <div className="input-group">
            <label htmlFor="news-input" className="input-label">
                News Content
            </label>
            <textarea
                id="news-input"
                className="text-area"
                placeholder="Paste news content here to analyze its credibility using AI..."
                value={value}
                onChange={(e) => onChange(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
            />
            <button
                className="analyze-button"
                style={{ marginTop: '24px' }}
                onClick={onAnalyze}
                disabled={disabled || !value.trim()}
            >
                {loading ? (
                    'Analyzing Content...'
                ) : (
                    'Verify Credibility'
                )}
            </button>
        </div>
    );
}

export default TextInput;
