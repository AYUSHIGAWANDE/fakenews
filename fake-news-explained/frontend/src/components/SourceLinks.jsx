import React from 'react';

/**
 * SourceLinks Component
 */
function SourceLinks({ sources }) {
    if (!sources || sources.length === 0) {
        return null;
    }

    const sourceUrls = {
        'FactCheck.org': 'https://www.factcheck.org',
        'Snopes': 'https://www.snopes.com',
        'PolitiFact': 'https://www.politifact.com',
        'Reuters': 'https://www.reuters.com',
        'Associated Press': 'https://apnews.com',
        'BBC News': 'https://www.bbc.com/news',
        'WHO': 'https://www.who.int',
        'CDC': 'https://www.cdc.gov',
        'NIH': 'https://www.nih.gov',
        'Nature': 'https://www.nature.com',
        'Science Magazine': 'https://www.science.org'
    };

    return (
        <div className="source-links">
            <h4 style={{ color: 'var(--text-dim)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '0.1em', marginBottom: '16px' }}>
                Trusted Verification Sources
            </h4>
            <div className="sources-grid">
                {sources.map((source, index) => {
                    const name = typeof source === 'string' ? source : source.name;
                    const url = typeof source === 'string' ? sourceUrls[source] : source.url;

                    return (
                        <a
                            key={index}
                            href={url || '#'}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="source-link"
                        >
                            <span className="source-name">{name}</span>
                            <span className="external-icon" style={{ marginLeft: 'auto', opacity: 0.5 }}>↗</span>
                        </a>
                    );
                })}
            </div>
        </div>
    );
}

export default SourceLinks;
