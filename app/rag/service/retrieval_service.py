from app.document.input_normalizer.text_normalizer import normalize_text
from app.rag.schema.retrieval_schema import (
    QuerySchema,
    QueryRecord,
    RetrievalRow,
    RetrievalResponse
)
from app.rag.components.embedder.text_embedder import embed_the_query
from app.rag.config.embedder_config import TIMEOUT, COLLECTION_NAME
from app.rag.config.retrieval_config import TOP_K
from app.rag.repository.retrieval_repository import (
    insert_query,
    retrieve_chunks,
    insert_retrieved_chunks,
)
from app.core.vector_normalizer import normalize


def retrieve_data(query: QuerySchema):
    normalized_query_content = normalize_text(query.content)
    stored_query = QueryRecord(**insert_query(normalized_query_content))
    query_embedding = embed_the_query(stored_query.content, TIMEOUT)
    query_embedding = normalize(query_embedding)
    retrieved_chunks = retrieve_chunks(query_embedding, COLLECTION_NAME, TOP_K)
    retrieved_chunks_with_query_id = attach_query_id_to_retrieved_chunks(
        retrieved_chunks,
        stored_query.query_id,
    )
    rows = insert_retrieved_chunks(retrieved_chunks_with_query_id)

    return RetrievalResponse(query=normalized_query_content, context=rows)


def attach_query_id_to_retrieved_chunks(chunks, query_id):
    rows = []

    for chunk in chunks:
        row = RetrievalRow(
            query_id=str(query_id),
            content=chunk.payload["content"],
            content_hash=chunk.payload["content_hash"],
            chunk_id=str(chunk.id),
            document_id=str(chunk.payload["document_id"]),
            vector_score=float(chunk.score),
        )
        rows.append(row)

    return rows
