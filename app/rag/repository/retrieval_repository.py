from uuid import UUID

from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny,
    MatchValue,
)

from app.database.postgres import pool
from app.database.vector_db import qdrant_client
from app.rag.schema.retrieval_schema import (
    QuerySchema,
    RerankedChunkList,
    RetrievalBody,
)


# ==========================================================
# QUERIES
# ==========================================================

async def insert_query(query: QuerySchema):
    query_sql = """
    INSERT INTO query (
        content,
        user_id,
        tenant_id
    )
    VALUES (%s, %s, %s)
    RETURNING *
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                query_sql,
                (
                    query.content,
                    query.user_id,
                    query.tenant_id,
                ),
            )
            return await cur.fetchone()


# ==========================================================
# RETRIEVED CHUNKS
# ==========================================================

async def insert_retrieved_chunks(
    retrieved_chunks: list[RetrievalBody],
):

    query_sql = """
    INSERT INTO retrieved_chunks (
        query_id,
        chunk_id,
        document_id,
        vector_score,
        user_id,
        tenant_id
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.executemany(
                query_sql,
                [
                    (
                        chunk.query_id,
                        chunk.chunk_id,
                        chunk.document_id,
                        chunk.vector_score,
                        chunk.user_id,
                        chunk.tenant_id
                    )
                    for chunk in retrieved_chunks
                ],
            )

        await conn.commit()

    return True


# ==========================================================
# RERANKED CHUNKS
# ==========================================================

async def insert_reranked_chunks(
    reranked_chunks: RerankedChunkList,
):
    query_sql = """
    INSERT INTO reranked_chunks (
        query_id,
        document_id,
        retrieved_chunk_id,
        chunk_id,
        reranked_score,
        user_id,
        tenant_id
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING reranked_chunk_id, query_id, document_id, retrieved_chunk_id, chunk_id, reranked_score, user_id, tenant_id
    """

    rows = [
        (
            chunk.query_id,
            chunk.document_id,
            chunk.retrieved_chunk_id,
            chunk.chunk_id,
            chunk.reranked_score,
            chunk.user_id,
            chunk.tenant_id,
        )
        for chunk in reranked_chunks.chunks
    ]
    inserted = []
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.executemany(
                query_sql,
                rows,
                returning=True
            )
            while True:
                inserted.extend(await cur.fetchall())
                if not cur.nextset():
                    break

        await conn.commit()

    return inserted


# ==========================================================
# VECTOR RETRIEVAL
# ==========================================================

def retrieve_embeddings(
    query_vector: list[float],
    collection_name: str,
    document_ids: list[UUID] | None,
    top_k_retrieval: int,
    user_id: UUID,
    tenant_id: UUID,
):
    must_conditions = [
        FieldCondition(
            key="tenant_id",
            match=MatchValue(value=str(tenant_id)),
        ),
        FieldCondition(
            key="user_id",
            match=MatchValue(value=str(user_id)),
        ),
    ]

    if document_ids:
        must_conditions.append(
            FieldCondition(
                key="document_id",
                match=MatchAny(
                    any=[
                        str(doc_id)
                        for doc_id in document_ids
                    ]
                ),
            )
        )

    response = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k_retrieval,
        query_filter=Filter(
            must=must_conditions
        ),
    )

    return response.points


# ==========================================================
# FETCH RETRIEVED CHUNKS BY QUERY
# ==========================================================

async def retrieve_chunks_with_chunk_content_from_query_id(
    query_id: UUID,
    user_id: UUID,
    tenant_id: UUID,
):
    query_sql = """
    SELECT
        rc.*,
        c.content
    FROM retrieved_chunks rc
    JOIN chunks c
        ON rc.chunk_id = c.chunk_id
    WHERE rc.query_id = %s
      AND rc.user_id = %s
      AND rc.tenant_id = %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                query_sql,
                (
                    query_id,
                    user_id,
                    tenant_id,
                ),
            )

            return await cur.fetchall()


# ==========================================================
# FETCH CHUNKS BY CHUNK IDS
# ==========================================================

async def retrieve_chunks_with_chunk_content(
    chunk_ids: list[UUID],
    user_id: UUID,
    tenant_id: UUID,
):
    query_sql = """
    SELECT
        rc.*,
        c.content
    FROM retrieved_chunks rc
    JOIN chunks c
        ON rc.chunk_id = c.chunk_id
    WHERE rc.chunk_id = ANY(%s)
      AND rc.user_id = %s
      AND rc.tenant_id = %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                query_sql,
                (
                    chunk_ids,
                    user_id,
                    tenant_id,
                ),
            )

            return await cur.fetchall()


# ==========================================================
# TOP RETRIEVED CHUNKS
# ==========================================================

async def fetch_top_retrieved_chunks(
    query_id: UUID,
    top_k: int,
    user_id: UUID,
    tenant_id: UUID,
):
    query_sql = """
    SELECT
        rc.*,
        c.content
    FROM retrieved_chunks rc
    JOIN chunks c
        ON rc.chunk_id = c.chunk_id
    WHERE rc.query_id = %s
      AND rc.user_id = %s
      AND rc.tenant_id = %s
    ORDER BY rc.vector_score DESC
    LIMIT %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                query_sql,
                (
                    query_id,
                    user_id,
                    tenant_id,
                    top_k,
                ),
            )

            return await cur.fetchall()