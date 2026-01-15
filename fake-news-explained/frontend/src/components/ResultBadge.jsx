import React from 'react';

/**
 * ResultBadge Component
 * Displays the classification result with color-coded badge
 */
function ResultBadge({ label }) {
    const getBadgeConfig = () => {
        switch (label) {
            case 'Likely Fake':
                return {
                    className: 'fake',
                    icon: '🔴',
                    text: 'Likely Fake'
                };
            case 'Unverified':
                return {
                    className: 'unverified',
                    icon: '🟡',
                    text: 'Unverified'
                };
            case 'Likely Real':
                return {
                    className: 'real',
                    icon: '🟢',
                    text: 'Likely Real'
                };
            default:
                return {
                    className: 'unverified',
                    icon: '❓',
                    text: 'Unknown'
                };
        }
    };

    const config = getBadgeConfig();

    return (
        <div className={`result-badge ${config.className}`}>
            <span className="badge-icon">{config.icon}</span>
            <span className="badge-text">{config.text}</span>
        </div>
    );
}

export default ResultBadge;
