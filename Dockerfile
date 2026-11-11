# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/hf-cache

WORKDIR /app

# 1) CPU-only PyTorch first: the default wheel pulls ~2 GB of CUDA libraries we don't need.
#    sentence-transformers (from requirements.txt) will then reuse this install.
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# 2) Dependencies before source code, so code edits don't re-run the install layer
COPY requirements.txt .
RUN pip install -r requirements.txt

# 3) Bake the embedding model into the image: no download at startup,
#    and no dependency on Hugging Face being reachable when the container starts
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# 4) Application code
COPY . .

# 5) Run as a non-root user; vector_db is where the FAISS indexes are persisted
RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/vector_db \
    && chown -R app:app /app /opt/hf-cache
USER app

EXPOSE 8000

# Python is already in the image, so no curl needed for the health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status == 200 else 1)"

# Single worker on purpose: api.py keeps an in-memory cache of loaded vector stores
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]