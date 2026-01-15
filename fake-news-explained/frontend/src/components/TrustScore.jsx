import React from 'react';

/**
 * TrustScore Component
 * Animated progress bar showing trust score (0-100)
 */
function TrustScore({ score, label }) {
    const getScoreClass = () => {
        if (score >= 70) return 'real';
        if (score >= 40) return 'unverified';
        return 'fake';
    };

    const scoreClass = getScoreClass();

    return (
        <div className="trust-score">
            <div className="score-header">
                <span className="score-label">Trust Score</span>
                <span className={`score-value ${scoreClass}`}>{score}/100</span>
            </div>
            <div className="score-bar">
                <div
                    className={`score-fill ${scoreClass}`}
                    style={{ width: `${score}%` }}
                />
            </div>
        </div>
    );
}

export default TrustScore;
