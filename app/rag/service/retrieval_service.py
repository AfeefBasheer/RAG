from app.document.input_normalizer.text_normalizer import normalize_text
from app.rag.schema.retrieval_schema import (
    QueryRequestSchema,
    QueryRecord,
    QuerySchema,
    RetrievalBody,
    RetrievalResponse,
    RerankedChunkList,
    RerankedResponse
)


from uuid import UUID
from app.rag.components.embedder.text_embedder import embed_the_query
from app.rag.config.embedder_config import TIMEOUT, COLLECTION_NAME
from app.rag.config.retrieval_config import (
    TOP_K_RETRIEVAL,
    TOP_K_RERANKED,
    RERANK_THRESHOLD,
    FALLBACK_TOP_K,
    RERANKER_TIMEOUT,
)
from app.rag.repository.retrieval_repository import (
    insert_query,
    retrieve_embeddings,
    insert_retrieved_chunks,
    insert_reranked_chunks,
    retrieve_chunks_with_chunk_content_from_query_id,
    fetch_top_retrieved_chunks,
)
from app.core.vector_normalizer import normalize
from app.rag.components.reranker.vector_reranker import rerank_the_vector


async def retrieve_data(query: QueryRequestSchema, user_id: UUID, tenant_id: UUID):
    normalized_query_content = normalize_text(query.content)
    normalized_query = QuerySchema(
        content=normalized_query_content, user_id=user_id, tenant_id=tenant_id
    )
    stored_query = QueryRecord(**await insert_query(normalized_query))
    query_embedding = embed_the_query(stored_query.content, TIMEOUT)
    query_embedding = normalize(query_embedding)
    retrieved_embeddings = retrieve_embeddings(
        query_embedding,
        COLLECTION_NAME,
        query.document_ids,
        TOP_K_RETRIEVAL,
        user_id,
        tenant_id,
    )

    retrieved_chunks_with_query_id = attach_query_id_to_retrieved_chunks(
        retrieved_embeddings,
        stored_query.query_id,
        user_id,
        tenant_id,
    )

    if not retrieved_chunks_with_query_id:
        return RetrievalResponse(
            query=normalized_query_content, context=[], reranked_chunks=False
        )

    await insert_retrieved_chunks(retrieved_chunks_with_query_id)
    reranked_chunks_with_content = None
    try:
        # raise Exception("Reranking failed due to timeout")  # Simulating reranking failure for testing fallback mechanism
        retrieved_chunks_with_content = await (
            retrieve_chunks_with_chunk_content_from_query_id(
                stored_query.query_id, user_id, tenant_id
            )
        )
        chunk_contents = extract_chunk_content_reranking(retrieved_chunks_with_content)
        reranked_chunks = rerank_the_vector(
            normalized_query_content, chunk_contents, RERANKER_TIMEOUT
        )
        normalized_chunks = normalize_reranked_chunks(
            reranked_chunks, retrieved_chunks_with_content, TOP_K_RERANKED, RERANK_THRESHOLD
        )
        reranked_chunks_with_query_id = attach_query_id_to_reranked_chunks(
            stored_query.query_id, normalized_chunks, user_id, tenant_id
        )
        reranked_chunks_row = RerankedChunkList(chunks=reranked_chunks_with_query_id)
        reranked_chunks_response = await insert_reranked_chunks(reranked_chunks_row)
        reranked_chunks_with_content = attach_content_to_reranked_chunks(reranked_chunks_response, retrieved_chunks_with_content)

    except Exception as error:
        print("reranking failed", error)

    if reranked_chunks_with_content:
        return RerankedResponse(
            query=normalized_query_content,
            context=reranked_chunks_with_content,
            reranked_chunks=True,
        )

    top_fall_back_retrieved_chunks = await fetch_top_retrieved_chunks(
        stored_query.query_id, FALLBACK_TOP_K, user_id, tenant_id
    )

    return RetrievalResponse(
        query=normalized_query_content,
        context=top_fall_back_retrieved_chunks,
        reranked_chunks=False,
    )

def attach_content_to_reranked_chunks(reranked_chunks_response, retrieved_chunks_with_content):
    retrieved_chunks_dict = {
    }
    for chunk in retrieved_chunks_with_content:
        chunk_id_str = str(chunk["chunk_id"])
        retrieved_chunks_dict[chunk_id_str] = chunk["content"]
    for chunk in reranked_chunks_response:
        chunk_id_str = str(chunk["chunk_id"])
        chunk["content"] = retrieved_chunks_dict.get(chunk_id_str, "")
    return reranked_chunks_response


def attach_query_id_to_retrieved_chunks(
    embeddings,
    query_id,
    user_id,
    tenant_id,
):
    rows = []
    for embedding in embeddings:
        row = RetrievalBody(
            query_id=str(query_id),
            user_id=str(user_id),
            tenant_id=str(tenant_id),
            chunk_id=embedding.id,
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


def normalize_reranked_chunks(
    reranked_chunks,
    retrieved_chunks_with_content,
    TOP_K_RERANKED,
    RERANK_THRESHOLD,
):

    selected_chunks = []
    for item in reranked_chunks:
        if len(selected_chunks) >= TOP_K_RERANKED:
            break
        if item["score"] >= RERANK_THRESHOLD:
            selected_chunks.append(item)
    normalized_chunks = []

    for item in selected_chunks:
        chunk = retrieved_chunks_with_content[item["index"]].copy()
        chunk["reranked_score"] = item["score"]
        normalized_chunks.append(chunk)
    return normalized_chunks

def attach_query_id_to_reranked_chunks(
    query_id: UUID, normalized_reranked_chunks: list, user_id: UUID, tenant_id: UUID
):
    reranked_chunks = []
    for item in normalized_reranked_chunks:
        chunk = {
            "query_id": query_id,
            "retrieved_chunk_id": item["retrieved_chunk_id"],
            "chunk_id": item["chunk_id"],
            "user_id": user_id,
            "tenant_id": tenant_id,
            "document_id": item["document_id"],
            "reranked_score":item["reranked_score"]
        }
        reranked_chunks.append(chunk)

    return reranked_chunks


def extract_chunk_content_reranking(db_chunks: list) -> list:
    return [
        chunk["content"]
        for chunk in db_chunks
        if chunk.get("content")
    ]
