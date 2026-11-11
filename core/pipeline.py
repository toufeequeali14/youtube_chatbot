import os

from common.config import VECTOR_DB_DIR
from ingestion.fetcher import get_video_transcript
from ingestion.chunker import split_transcripts
from retrieval.embeddings import build_vector_store, save_vector_store, load_vector_store


def get_or_build_vector_store(video_id: str):
    path = os.path.join(VECTOR_DB_DIR, video_id)  # one index per video

    if os.path.exists(path):
        return load_vector_store(path)

    transcript = get_video_transcript(video_id=video_id)
    chunks = split_transcripts(video_transcripts=transcript)
    vector_store = build_vector_store(chunks)
    save_vector_store(vector_store, path)
    return vector_store

