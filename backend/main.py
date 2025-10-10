# backend/main.py
import os
import io
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cassio
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Cassandra
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# --- INITIALIZE MODELS AND DATABASE ON STARTUP ---
try:
    ASTRA_DB_TOKEN = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
    ASTRA_DB_ID = os.environ["ASTRA_DB_ID"]
    GOOGLE_API_KEY = os.environ["GOOGLE_AI_KEY"]

    cassio.init(token=ASTRA_DB_TOKEN, database_id=ASTRA_DB_ID)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=GOOGLE_API_KEY)
    vector_store = Cassandra(embedding=embedding_model, table_name="pdf_api_store")

except KeyError as e:
    print(f"CRITICAL ERROR: Environment variable {e} not set.")
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

# NEW: Endpoint for uploading and processing the PDF
@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not vector_store:
        raise HTTPException(status_code=500, detail="Server is not configured correctly.")
    
    try:
        pdf_bytes = await file.read()
        
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_stream)
        raw_text = ''.join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = text_splitter.split_text(raw_text)
        
        # Clear the old data and add the new data
        vector_store.clear()
        vector_store.add_texts(chunks)
        
        return {"message": f"Successfully processed '{file.filename}'. Vector DB is ready to query."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pydantic model for the query request body
class QueryRequest(BaseModel):
    question: str

# NEW: Endpoint for asking questions
@app.post("/query/")
async def process_query(request: QueryRequest):
    if not llm or not vector_store:
        raise HTTPException(status_code=500, detail="Server is not configured correctly.")

    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )
        answer = qa_chain.run(request.question)
        return {"answer": answer}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "CogniDoc backend is running."}