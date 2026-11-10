# Entry point (CLI, FastAPI server, or Streamlit UI)

import os
import warnings

# Suppress Hugging Face unauthenticated request warnings and other warnings
os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)


from ingestion.fetcher import get_video_transcript
from ingestion.chunker import split_transcripts
from retrieval.embeddings import make_embeddings

if __name__ == '__main__':
    video_id = "Gfr50f6ZBvo"

    video_transcripts = get_video_transcript(video_id=video_id)

    transcripts_chunks = split_transcripts(video_transcripts=video_transcripts)

    print(f"no of chunks: {len(transcripts_chunks)} \n chunk-60: {transcripts_chunks[59]}")

    vector_store = make_embeddings(transcripts_chunks)

    # Check the total number of vectors stored in the FAISS database
    print(f"Vector store successfully created with {vector_store.index.ntotal} vectors indexed!")