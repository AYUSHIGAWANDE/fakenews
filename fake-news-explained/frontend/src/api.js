/**
 * API Handler for Fake News Explained
 * Centralized API communication with the backend
 */

const API_BASE_URL = 'http://localhost:5000';

/**
 * Analyze news text for fake news indicators
 * @param {string} text - The news text to analyze
 * @returns {Promise<Object>} Analysis results
 */
export async function analyzeNews(text) {
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to analyze text');
        }

        return await response.json();
    } catch (error) {
        // Handle network errors
        if (error.message === 'Failed to fetch') {
            throw new Error('Unable to connect to the server. Please make sure the backend is running.');
        }
        throw error;
    }
}

/**
 * Check if the API is healthy
 * @returns {Promise<boolean>} True if API is healthy
 */
export async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch {
        return false;
    }
}

export default { analyzeNews, checkHealth };
