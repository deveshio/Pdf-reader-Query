// src/components/QueryForm.js
import React, { useState } from 'react';
import { queryDoc } from '../services/api';
import ReactMarkdown from 'react-markdown'; 

function QueryForm() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!question) return;

        setLoading(true);
        setError('');
        setAnswer('');

        try {
            const data = await queryDoc(question);
            setAnswer(data.answer);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
       <div className="query-container">
            <form onSubmit={handleSubmit} className="query-form">
                <div className="input-wrapper">
                    <label>Ask a Question</label>
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="e.g., What is the main topic of the document?"
                        disabled={loading}
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Thinking...' : 'Get Answer'}
                </button>
            </form>

            {loading && <p className="status-text">Getting your answer...</p>}
            {error && <div className="error-box">{error}</div>}
            
            {answer && (
                // NEW: A styled "card" for the answer
                <div className="answer-card">
                    <h3>Answer</h3>
                    <ReactMarkdown>{answer}</ReactMarkdown>
                </div>
            )}
        </div>
    );
}

export default QueryForm;