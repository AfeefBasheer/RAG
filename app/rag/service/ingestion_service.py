from app.rag.components.embedder.text_embedder import embed_the_chunks
from app.rag.service.embedding_service import check_embeddings
from app.rag.components.text_splitter.chunker import chunk_data_by_chars

from app.document.service.document_service import (
    get_document_by_document_id,
    mark_document_chunked,
    mark_document_embedded,
)
from app.document.service.chunk_service import insert_chunks, get_chunks_by_document_id
from app.rag.service.embedding_service import insert_embeddings

from app.rag.config.text_splitter_config import CHUNK_SIZE_v1, OVERLAP_SIZE_v1
from app.rag.config.embedder_config import TIMEOUT, COLLECTION_NAME
from uuid import UUID


def ingest_document(document_id: UUID):
    document = get_document_by_document_id(document_id)
    if not document.document_id == document_id:
        raise "Document Doesn't Exist"

    chunk_response = get_chunks_by_document_id(document_id)
    if not chunk_response:
        raw_chunks = chunk_data_by_chars(
            document.content, CHUNK_SIZE_v1, OVERLAP_SIZE_v1
        )
        chunk_response = insert_chunks(document_id, raw_chunks)
        if chunk_response:
            mark_document_chunked(document_id)

    chunks = extract_chunk_content(chunk_response)
    embedded_data = check_embeddings(COLLECTION_NAME, document_id, len(chunks))
    if not embedded_data:
        embeddings = embed_the_chunks(chunks, TIMEOUT)
        embed_response = insert_embeddings(COLLECTION_NAME, chunk_response, embeddings)
        if embed_response:
            mark_document_embedded(document_id)

    return get_document_by_document_id(document_id)


def extract_chunk_content(db_chunks: list) -> list:
    return [chunk["content"] for chunk in db_chunks]
