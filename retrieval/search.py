# retrieval.search.py
from common.config import TOP_K


def retrieve(vector_store, question, k=TOP_K):
    similarity_retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": k}
    )
    return similarity_retriever.invoke(question)
