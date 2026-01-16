from app.rag.input_normalizer.text import normalize_data
from app.rag.embedder.text_embedder import embed_the_chunks
from app.rag.text_splitter.chunker import chunk_data
from app.rag.config.text_splitter import CHUNK_SIZE_v1,OVERLAP_SIZE_v1

def ingest(ingestion_data):
    text = normalize_data(ingestion_data.text)
    chunked_data = chunk_data(text,CHUNK_SIZE_v1,OVERLAP_SIZE_v1)
    embedded_data = embed_the_chunks(chunked_data)
    return embedded_data
