# Text splitting and semantic chunking strategies
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingestion.fetcher import get_video_transcript

def split_transcripts(video_transcripts: list = None) -> list:

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([video_transcripts])


    return chunks
