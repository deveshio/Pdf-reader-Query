// src/components/FileUploader.js
import React, { useState } from 'react';
import { uploadPdf } from '../services/api';

function FileUploader({ onUploadSuccess }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');

    const handleFileChange = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setLoading(true);
        setError('');
        setMessage(`Processing '${file.name}'...`);

        try {
            const data = await uploadPdf(file);
            setMessage(data.message);
            onUploadSuccess(true); // Tell the parent component the DB is ready
        } catch (err) {
            setError(err.message);
            onUploadSuccess(false);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="file-uploader">
            <label>1. Upload PDF:</label>
            <input type="file" accept=".pdf" onChange={handleFileChange} disabled={loading} />
            {loading && <p>{message}</p>}
            {error && <div className="error">{error}</div>}
            {!loading && message && <p className="success">{message}</p>}
        </div>
    );
}

export default FileUploader;