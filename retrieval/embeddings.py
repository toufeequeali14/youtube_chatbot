# retrieval/embeddings.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import os
import warnings

# Suppress Hugging Face unauthenticated request warnings and other warnings
os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)

def make_embeddings(transcripts_chunks: list = None):
    # Use the full model identifier and model_name parameter
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Correctly build the FAISS vector store using the chunks and embeddings
    vector_store = FAISS.from_documents(transcripts_chunks, embeddings)

    print(f"Vector store successfully created with {len(transcripts_chunks)} chunks indexed!")

    return vector_store