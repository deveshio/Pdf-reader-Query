cognidoc/
│
├── 📂 backend/
│   ├── 📄 main.py                 # Your FastAPI application logic
│   ├── 📄 requirements.txt        # Python dependencies for the backend
│   ├── 📄 .env                    # Your secret keys for local development
│   └── 📄 .gitignore              # Ignores files like .venv, .env and __pycache__
│
├── 📂 frontend/
│   ├── 📂 public/
│   │   └── 📄 index.html          # The main HTML page for your React app
│   │
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── 📄 FileUploader.js # React component for the file upload UI
│   │   │   └── 📄 QueryForm.js    # React component for the question form
│   │   │
│   │   ├── 📂 services/
│   │   │   └── 📄 api.js          # Handles all API calls to the backend
│   │   │
│   │   ├── 📄 App.js              # Main component, orchestrates the UI
│   │   ├── 📄 App.css             # Styles for the main App component
│   │   ├── 📄 index.js            # The entry point for your React app
│   │   └── 📄 index.css           # Global styles for your app
│   │
│   ├── 📄 package.json            # Lists the frontend's dependencies
│   ├── 📄 package-lock.json       # Locks dependency versions
│   └── 📄 .gitignore              # Ignores files like node_modules
│
├── 📄 .gitignore                  # Root .gitignore for general ignores
└── 📄 README.md                   # Project description and setup instructions