try:
    import pyasyncore as asyncore
    import sys
    sys.modules['asyncore'] = asyncore
except ImportError:
    pass

import os
import io
# ... the rest of your imports
import os
import io
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cassio
from PyPDF2 import PdfReader

# --- UPDATED IMPORTS FOR LANGCHAIN v0.1+ ---
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Cassandra
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA

# --- INITIALIZE MODELS AND DATABASE ON STARTUP ---
try:
    # Ensure these match exactly with your Render Environment Variable Keys
    ASTRA_DB_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_ID = os.environ.get("ASTRA_DB_ID")
    GOOGLE_API_KEY = os.environ.get("GOOGLE_AI_KEY")

    if not all([ASTRA_DB_TOKEN, ASTRA_DB_ID, GOOGLE_API_KEY]):
        raise KeyError("One or more required environment variables are missing.")

    # Initialize Cassio (The handshake with Astra DB)
    cassio.init(token=ASTRA_DB_TOKEN, database_id=ASTRA_DB_ID)
    
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Updated to gemini-1.5-flash as gemini-2.5 does not exist yet!
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    
    # Corrected Vector Store Initialization
    vector_store = Cassandra(
        embedding=embedding_model, 
        table_name="pdf_api_store",
        session=None, # Cassio manages this globally after cassio.init()
        keyspace=None  # Uses default keyspace from Astra
    )

except Exception as e:
    print(f"CRITICAL ERROR DURING STARTUP: {str(e)}")
    embedding_model, llm, vector_store = None, None, None

# --- FASTAPI APP SETUP ---
app = FastAPI(title="CogniDoc Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API ENDPOINTS ---

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not vector_store:
        raise HTTPException(status_code=500, detail="Vector Store not initialized. Check server logs.")
    
    try:
        pdf_bytes = await file.read()
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_stream)
        
        # Improved text extraction
        text_content = []
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
        
        raw_text = " ".join(text_content)
        
        if not raw_text.strip():
            raise ValueError("The PDF appears to be empty or contains no extractable text.")
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = text_splitter.split_text(raw_text)
        
        # Using add_texts is safer than clearing if you want high availability
        # vector_store.clear() # Uncomment if you specifically want to wipe old PDFs every time
        vector_store.add_texts(chunks)
        
        return {"message": f"Successfully processed '{file.filename}'. {len(chunks)} chunks added."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing Error: {str(e)}")

class QueryRequest(BaseModel):
    question: str

@app.post("/query/")
async def process_query(request: QueryRequest):
    if not llm or not vector_store:
        raise HTTPException(status_code=500, detail="LLM or Vector Store not initialized.")

    try:
        # RetrievalQA still works, but requires the retriever from the vector_store
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )
        
        # Updated from .run() to .invoke() (Modern LangChain standard)
        response = qa_chain.invoke({"query": request.question})
        return {"answer": response["result"]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query Error: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "CogniDoc backend is running."}