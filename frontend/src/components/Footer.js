import React from 'react';

// --- Icons ---
const GithubIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
);

const LinkedinIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
);

const KaggleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 22h-4.5l-7-10 7-10H22" /><path d="M2 2v20" /><path d="M10 12H2" /></svg>
);

const ExternalLinkIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
);

export default function Footer() {
  return (
    <footer className="split-footer">
      <div className="footer-container">
        
        {/* LEFT SIDE: Connections */}
        <div className="footer-left">
          <span className="footer-label">Connect:</span>
          <div className="social-icons">
            <a href="https://github.com/deveshio" target="_blank" rel="noreferrer" title="GitHub">
              <GithubIcon />
            </a>
            <a href="https://linkedin.com/in/devesh-suthar-" target="_blank" rel="noreferrer" title="LinkedIn">
              <LinkedinIcon />
            </a>
            <a href="https://kaggle.com/deveshsuthar" target="_blank" rel="noreferrer" title="Kaggle">
              <KaggleIcon />
            </a>
          </div>
        </div>

        {/* RIGHT SIDE: Project Links + More Projects */}
        <div className="footer-right">
          <a href="https://github.com/deveshio/Pdf-reader-Query" className="project-link" target="_blank" rel="noreferrer">
            Source Code
          </a>
          <a href="https://www.kaggle.com/code/deveshsuthar/customer-churn-project" className="project-link" target="_blank" rel="noreferrer">
            Kaggle Notebook
          </a>
          
          {/* The "Space" / Divider */}
          <span className="divider">|</span>
          
          <a href="https://deveshio.notion.site/Devesh-Kumar-Suthar-1f353329aa5f80198193f292a4d27ce4?v=29753329aa5f8093a2e5000ce481f005" className="more-projects-link" target="_blank" rel="noreferrer">
            More Projects <ExternalLinkIcon />
          </a>
        </div>

      </div>
    </footer>
  );
}