from app.document.input_normalizer.text_normalizer import normalize_text
from app.rag.schema.retrieval_schema import (
    QueryRequestSchema,
    QueryRecord,
    QuerySchema,
    RetrievalRow,
    RetrievalResponse,
)
from uuid import UUID
from app.rag.components.embedder.text_embedder import embed_the_query
from app.rag.config.embedder_config import TIMEOUT, COLLECTION_NAME
from app.rag.config.retrieval_config import TOP_K
from app.rag.repository.retrieval_repository import (
    insert_query,
    retrieve_embeddings,
    insert_retrieved_chunks,
)
from app.core.vector_normalizer import normalize
from app.document.service.chunk_service import retrieve_chunks

def retrieve_data(query: QueryRequestSchema, user_id:UUID,tenant_id: UUID):
    normalized_query_content = normalize_text(query.content)
    normalized_query = QuerySchema(
        content=normalized_query_content, user_id = user_id,tenant_id=tenant_id
    )
    stored_query = QueryRecord(**insert_query(normalized_query))
    query_embedding = embed_the_query(stored_query.content, TIMEOUT)
    query_embedding = normalize(query_embedding)
    retrieved_embeddings = retrieve_embeddings(query_embedding, COLLECTION_NAME, TOP_K,user_id,tenant_id)
    chunk_ids = get_chunk_ids(retrieved_embeddings)
    retrieved_chunks = retrieve_chunks(chunk_ids,user_id,tenant_id)
    retrieved_chunks_with_query_id = attach_query_id_to_retrieved_chunks(
        retrieved_embeddings,
        retrieved_chunks,
        stored_query.query_id,
        user_id,
        tenant_id,
    )
    rows = insert_retrieved_chunks(retrieved_chunks_with_query_id)
    return RetrievalResponse(query=normalized_query_content, context=rows)


def attach_query_id_to_retrieved_chunks(embeddings,chunks, query_id,user_id,tenant_id):
    rows = []

    for embedding, chunk in zip(embeddings, chunks):
        row = RetrievalRow(
            query_id=str(query_id),
            user_id = str(user_id),
            tenant_id = str(tenant_id),
            content=chunk["content"],
            content_hash=chunk["content_hash"],
            chunk_id=str(chunk["chunk_id"]),
            document_id=str(embedding.payload["document_id"]),
            vector_score=float(embedding.score),
        )
        rows.append(row)
    return rows

def get_chunk_ids(embeddings):
    chunk_id = []
    for item in embeddings:
        chunk_id.append(item.id)
    return chunk_id
