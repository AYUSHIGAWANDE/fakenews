import React from 'react';

/**
 * ResultBadge Component
 */
function ResultBadge({ label }) {
    const getBadgeConfig = () => {
        const lowerLabel = label?.toLowerCase() || '';
        if (lowerLabel.includes('real') || lowerLabel.includes('true')) {
            return { className: 'real', text: 'VERIFIED CONTENT' };
        } else if (lowerLabel.includes('fake') || lowerLabel.includes('false')) {
            return { className: 'fake', text: 'SUSPICIOUS CONTENT' };
        }
        return { className: 'unverified', text: 'UNVERIFIED' };
    };

    const config = getBadgeConfig();

    return (
        <div className={`trust-badge ${config.className}`}>
            <span className="badge-text">{config.text}</span>
        </div>
    );
}

export default ResultBadge;
