from app.rag.components.embedder.text_embedder import embed_the_chunks
from app.rag.service.embedding_service import check_embeddings
from app.rag.components.text_splitter.chunker import chunk_data_by_sentence

from app.document.service.document_service import (
    get_document_by_document_id,
    mark_document_chunked,
    mark_document_embedded,
)
from app.document.service.chunk_service import (
    insert_chunks,
    fetch_chunks_by_document_id,
)
from app.rag.service.embedding_service import insert_embeddings

from app.rag.config.text_splitter_config import CHUNK_SIZE_v1, SENTENCE_OVERLAP_V1
from app.rag.config.embedder_config import TIMEOUT, COLLECTION_NAME
from uuid import UUID


def ingest_document(document_id: UUID, user_id: UUID, tenant_id: UUID):
    document = get_document_by_document_id(document_id, user_id, tenant_id)
    if not document.document_id == document_id:
        raise ValueError("Document Doesn't Exist") 

    chunk_response = fetch_chunks_by_document_id(document_id, user_id, tenant_id)
    if not chunk_response:
        raw_chunks = chunk_data_by_sentence(
            document.content, CHUNK_SIZE_v1, SENTENCE_OVERLAP_V1
        )
        chunk_response = insert_chunks(raw_chunks, document_id, user_id, tenant_id)
        if chunk_response:
            mark_document_chunked(document_id, user_id, tenant_id)

    chunks = extract_chunk_content(chunk_response)
    embedded_data = check_embeddings(
        len(chunks), COLLECTION_NAME, document_id, user_id, tenant_id
    )
    if not embedded_data:
        embeddings = embed_the_chunks(chunks, TIMEOUT)
        embed_response = insert_embeddings(
            COLLECTION_NAME, chunk_response, embeddings, user_id, tenant_id
        )
        if embed_response:
            mark_document_embedded(document_id, user_id, tenant_id)

    return get_document_by_document_id(document_id, user_id, tenant_id)


def extract_chunk_content(db_chunks: list) -> list:
    return [chunk["content"] for chunk in db_chunks]
