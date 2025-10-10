// src/App.js
import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import QueryForm from './components/QueryForm';

function App() {
    const [isDBReady, setIsDBReady] = useState(false);

    return (
        <div className="App">
            <header className="App-header">
                  <h1>
                    <span className="brand">CogniDoc</span>
                    <span className="tagline">Upload your PDF & ask questions</span>
                  </h1>
            </header>
            <div className="Main">
                {!isDBReady && <FileUploader onUploadSuccess={setIsDBReady} /> }
                {isDBReady && <QueryForm />}
              
            </div>
        </div>
    );
}

export default App;