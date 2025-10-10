// src/services/api.js

// const BACKEND_URL = 'http://localhost:8000'; // Change to your Render URL for production
const BACKEND_URL = 'https://cognidocbackend.onrender.com'; // Change to your Render URL for production

export const uploadPdf = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${BACKEND_URL}/upload`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to process PDF.');
    }

    return await response.json();
};

export const queryDoc = async (question) => {
    const response = await fetch(`${BACKEND_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
    });

    if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to get an answer.');
    }

    return await response.json();
};