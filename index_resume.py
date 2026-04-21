import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

# Load env vars
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "sourabh-resume-index"

# Load and split documents
pdf_loader = PyPDFLoader("Sourabh_Dandage_cv.pdf")
txt_loader = TextLoader("info.txt")
documents = pdf_loader.load() + txt_loader.load()
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)

# Gemini Embeddings (768 dimensions)
embedding = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# Create Pinecone index (only if not exists)
pc = Pinecone(api_key=PINECONE_API_KEY)
if INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Upload docs to Pinecone
vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=embedding,
    index_name=INDEX_NAME,
    pinecone_api_key=PINECONE_API_KEY
)

print("Resume successfully indexed in Pinecone!")
