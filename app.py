# ==============================================================================
# 1. IMPORTS AND APP SETUP
# ==============================================================================
import streamlit as st
import cassio
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Cassandra
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
import io

# --- App Configuration ---
st.set_page_config(
    page_title="CogniDoc",
    page_icon="📄",
    layout="centered"
)
st.title("📄 CogniDoc")
st.write("Upload your PDF document, and I'll answer your queries about it.")


# ==============================================================================
# 2. CACHED SETUP FOR MODELS AND DATABASE
# ==============================================================================
@st.cache_resource
def initialize_services():
    """
    Initializes the database connection and AI models.
    """
    cassio.init(
        token=st.secrets["ASTRA_DB_APPLICATION_TOKEN"],
        database_id=st.secrets["ASTRA_DB_ID"]
    )
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=st.secrets["GOOGLE_AI_KEY"])
    return embedding_model, llm

# CORRECTED THE CACHE DECORATOR HERE
@st.cache_resource(max_entries=5)
def create_rag_chain(_embedding_model, _llm, pdf_bytes):
    """
    Processes the uploaded PDF and creates the RAG chain.
    """
    # --- Load and Process PDF from Bytes ---
    pdf_stream = io.BytesIO(pdf_bytes)
    pdf_reader = PdfReader(pdf_stream)
    raw_text = ''.join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = text_splitter.split_text(raw_text)

    # --- Create and Populate Vector Store ---
    # --- Create and Populate Vector Store ---
    vector_store = Cassandra(embedding=_embedding_model, table_name="pdf_query_app_store_dynamic")
    # Add this line to delete all old entries
    vector_store.clear()
    # Now add the new chunks to the empty table
    vector_store.add_texts(chunks)

    # --- Create the QA Chain ---
    qa_chain = RetrievalQA.from_chain_type(
        llm=_llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    return qa_chain


# ==============================================================================
# 3. MAIN APP LOGIC
# ==============================================================================
try:
    embedding_model, llm = initialize_services()
except KeyError:
    st.error("One or more secrets are missing. Please add them to your .streamlit/secrets.toml file.")
    st.stop()
except Exception as e:
    st.error(f"Failed to initialize services. Error: {e}")
    st.stop()

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_bytes = uploaded_file.getvalue()
    
    with st.spinner("Analyzing your document... This may take a moment."):
        try:
            # The function now uses the corrected cache decorator
            qa_chain = create_rag_chain(embedding_model, llm, pdf_bytes)
            st.success("Document analyzed successfully! You can now ask questions.")
        except Exception as e:
            st.error(f"Failed to process the document. Error: {e}")
            st.stop()

    user_question = st.text_input("Ask a question about your document:")

    if user_question:
        with st.spinner("Thinking..."):
            try:
                answer = qa_chain.run(user_question)
                st.write("### Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"An error occurred while generating the answer: {e}")

else:
    st.info("Please upload a PDF file to get started.")