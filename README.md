# YouTube Video Chatbot (RAG)

Ask questions about any YouTube video. Answers are grounded in the video's transcript; if the transcript doesn't contain the answer, the bot says so.

**Stack:** Python · LangChain · FAISS · Sentence-Transformers (local embeddings) · Groq (LLM) · FastAPI · Docker

## How it works

```
video ID → fetch transcript → chunk → embed → FAISS index (cached per video)
question → top-k retrieval → prompt (rules + chunks + question) → LLM → answer
```

The first request for a video builds and saves its index (`vector_db/<video_id>`). Later requests reuse it.

## Run

Create a `.env` in the project root:

```
GROQ_API_KEY=your_key_here
```

**Docker**

```bash
docker compose up --build
```

**Local**

```bash
./run.sh          # Linux/macOS
run.bat           # Windows
```

The API is served at `http://localhost:8000` (interactive docs at `/docs`).

## Usage

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"video_id": "Gfr50f6ZBvo", "question": "what is deepmind?"}'
```

## Expected output

```json
{
  "video_id": "Gfr50f6ZBvo",
  "question": "what is deepmind?",
  "answer": "DeepMind is a research company that builds some of the most groundbreaking artificial-intelligence systems in computing history, such as AlphaZero and AlphaFold 2. ..."
}
```

`GET /health` returns `{"status": "ok"}`. Invalid video IDs return `400`; videos without a transcript return `404`.

## Configuration

Model names and retrieval settings live in `common/config.py`. Groq retires models from time to time; if you get `model_not_found`, update `LLM_MODEL` from Groq's current model list.
