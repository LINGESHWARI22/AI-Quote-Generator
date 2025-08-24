# embeddings.py
from dotenv import load_dotenv
import os
from huggingface_hub import login
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
import json

# Load environment variables from .env file
load_dotenv()

# Log in to Hugging Face using the token from .env
hf_token = os.getenv("HUGGING_FACE_TOKEN")
if hf_token:
    login(token=hf_token)

# Load service data from JSON
with open("data/services.json", "r", encoding="utf-8") as f:
    service_data = json.load(f)

# Load embeddings model from Hugging Face
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define a custom embedding function
class CustomEmbeddingFunction:
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        # Convert embeddings to list of lists (NOT numpy array)
        return [emb.tolist() for emb in self.model.encode(texts)]

    def embed_query(self, text):
        # For single query
        return self.model.encode([text])[0].tolist()

# Create an instance of the custom embedding function
embedding_function = CustomEmbeddingFunction(embedding_model)

# Create Chroma DB
vector_db = Chroma.from_texts(
    texts=[s["name"] for s in service_data],
    embedding=embedding_function,  # Pass the custom embedding function
    metadatas=service_data
)
