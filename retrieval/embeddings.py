# retrieval/embeddings.py
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from common.config import EMBEDDING_MODEL

os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def build_vector_store(chunks):
    return FAISS.from_documents(chunks, get_embedding_model())


def save_vector_store(vector_store, path):
    vector_store.save_local(path)


def load_vector_store(path):
    # Safe here because you created this file yourself
    return FAISS.load_local(
        path, get_embedding_model(), allow_dangerous_deserialization=True
    )
