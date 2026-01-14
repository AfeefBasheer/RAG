from app.rag.input_normalizer.text import normalize_data
from app.rag.text_splitter.chunker import split_data
from app.rag.config.text_splitter import CHUNK_SIZE_v1,OVERLAP_SIZE_v1

def ingest(ingestion_data):
    text = normalize_data(ingestion_data.text)
    chunked_data = split_data(text,CHUNK_SIZE_v1,OVERLAP_SIZE_v1)
    return chunked_data
    # embedded_data = data_embedder(chunked_data)
    # normalized_embedded_data = normalize_embedded_data(embedded_data)
    # response = store_embedded_data(normalized_embedded_data)
    # return response