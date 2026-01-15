import React from 'react';

/**
 * ExplanationBox Component
 */
function ExplanationBox({ explanations }) {
    if (!explanations || explanations.length === 0) {
        return null;
    }

    return (
        <div className="explanation-box">
            <h4 style={{ color: 'var(--text-dim)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '0.1em', marginBottom: '16px' }}>
                Flagged Analysis ({explanations.length})
            </h4>
            <div className="explanation-list">
                {explanations.map((item, index) => (
                    <div key={index} className="explanation-item">
                        <span className="explanation-sentence" style={{ borderLeft: '2px solid #ef4444', paddingLeft: '12px' }}>
                            {item.sentence}
                        </span>
                        <p className="explanation-reason">
                            {item.reason}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ExplanationBox;
