from app.rag.components.embedder.text_embedder import embed_the_chunks
from app.rag.service.embedding_service import check_embeddings
from app.rag.components.text_splitter.chunker import chunk_data_by_sentence

from app.document.service.document_service import (
    fetch_document_by_document_id,
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
from app.core.exception import JobFailureException
from worker.retry import classify_error_type
from app.queue.queue_service import enqueue_chunk_job, enqueue_embed_job


async def ingest_document(document_id: UUID, user_id: UUID, tenant_id: UUID):
    document = await fetch_document_by_document_id(document_id, user_id, tenant_id)

    if not document:
        raise JobFailureException(
            [
                {
                    "error": "Document not found",
                    "target": "get_document",
                    "type": "document not found",
                    "retry": False,
                }
            ]
        )

    response = await enqueue_chunk_job(document_id, user_id, tenant_id)
    return response


async def chunk_document(record):
    document_id = record.document_id
    user_id = record.user_id
    tenant_id = record.tenant_id

    document = await fetch_document_by_document_id(document_id, user_id, tenant_id)
    chunk_response = None

    try:
        chunk_response = await fetch_chunks_by_document_id(document_id, user_id, tenant_id)
        if not chunk_response:
            raw_chunks = chunk_data_by_sentence(
                document["content"], CHUNK_SIZE_v1, SENTENCE_OVERLAP_V1
            )
            await insert_chunks(raw_chunks, document_id, user_id, tenant_id)
        await mark_document_chunked(document_id, user_id, tenant_id)
    except Exception as e:
        raise JobFailureException(
            [
                {
                    "error": str(e),
                    "target": "chunking",
                    "type": type(e).__name__,
                    "retry": classify_error_type(e),
                }
            ]
        )
    response = await enqueue_embed_job(document_id, user_id, tenant_id)
    return response


async def embed_document(record):
    document_id = record.document_id
    user_id = record.user_id
    tenant_id = record.tenant_id

    chunk_response = await fetch_chunks_by_document_id(document_id, user_id, tenant_id)
    chunks = extract_chunk_content(chunk_response)
    if not chunks:
        raise JobFailureException(
            [
                {
                    "error": str(e),
                    "target": "embedding",
                    "type": type(e).__name__,
                    "retry": classify_error_type(e),
                }
            ]
        )

    try:
        embedded_data = check_embeddings(
            len(chunks), COLLECTION_NAME, document_id, user_id, tenant_id
        )
        if not embedded_data:
            embeddings = embed_the_chunks(chunks, TIMEOUT)
            embedded_data = insert_embeddings(
                COLLECTION_NAME, chunk_response, embeddings, user_id, tenant_id
            )

        if embedded_data:
            await mark_document_embedded(document_id, user_id, tenant_id)

    except Exception as e:
        print(e)
        raise JobFailureException(
            [
                {
                    "error": str(e),
                    "target": "embedding",
                    "type": type(e).__name__,
                    "retry": classify_error_type(e),
                }
            ]
        )

    return await fetch_document_by_document_id(document_id, user_id, tenant_id)


def extract_chunk_content(db_chunks: list) -> list:
    return [chunk["content"] for chunk in db_chunks]
