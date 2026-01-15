import React from 'react';

/**
 * SourceLinks Component
 * Clickable verification source links
 */
function SourceLinks({ sources }) {
    if (!sources || sources.length === 0) {
        return null;
    }

    // Default URLs for common sources
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

    const getSourceIcon = (name) => {
        if (name.includes('FactCheck') || name.includes('Snopes') || name.includes('PolitiFact')) {
            return '✅';
        }
        if (name.includes('WHO') || name.includes('CDC') || name.includes('NIH')) {
            return '🏥';
        }
        if (name.includes('Nature') || name.includes('Science')) {
            return '🔬';
        }
        return '📰';
    };

    return (
        <div className="source-links">
            <h3 className="section-title">
                <span className="section-icon">🔗</span>
                Verify With Trusted Sources
            </h3>
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
                            <span className="source-icon">{getSourceIcon(name)}</span>
                            <span className="source-name">{name}</span>
                            <span className="external-icon">↗</span>
                        </a>
                    );
                })}
            </div>
        </div>
    );
}

export default SourceLinks;
