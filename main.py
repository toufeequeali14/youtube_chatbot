# main.py
import common.config  # noqa: F401  (sets env vars before anything else loads)

from core.pipeline import get_or_build_vector_store
from core.rag_engine import answer_question

if __name__ == "__main__":
    vector_store = get_or_build_vector_store("Gfr50f6ZBvo")
    print(answer_question(vector_store, "what is deepmind?"))