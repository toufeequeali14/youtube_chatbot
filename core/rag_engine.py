# core/rag_engine.py
from langchain_groq import ChatGroq
from common.config import LLM_MODEL, GROQ_API_KEY
from retrieval.search import retrieve
from core.prompts import RAG_PROMPT

chat_model = ChatGroq(model=LLM_MODEL, temperature=0.2, api_key=GROQ_API_KEY)
# chat_model= ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)     # correct
# chat_model = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)             # correct
# chat_model = ChatGroq(model="llama-3.3-70b-versatile", api_key=OPENAI_API_KEY)   # fails, wrong provider's key

def answer_question(vector_store, question):
    relevant_docs = retrieve(vector_store, question)
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    prompt_value = RAG_PROMPT.invoke({"context": context, "question": question})
    response = chat_model.invoke(prompt_value)
    return response.content