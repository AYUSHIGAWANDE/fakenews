import React from 'react';

/**
 * ExplanationBox Component
 * Expandable panel showing sentence-level explanations
 */
function ExplanationBox({ explanations }) {
    if (!explanations || explanations.length === 0) {
        return null;
    }

    return (
        <div className="explanation-box">
            <h3 className="section-title">
                <span className="section-icon">⚠️</span>
                Flagged Content ({explanations.length})
            </h3>
            <div className="explanation-list">
                {explanations.map((item, index) => (
                    <div key={index} className="explanation-item">
                        <p className="explanation-sentence">"{item.sentence}"</p>
                        <p className="explanation-reason">
                            <span className="reason-icon">💡</span>
                            {item.reason}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ExplanationBox;
