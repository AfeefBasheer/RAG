from uuid import UUID

from app.database.postgres import pool


async def create_chunks(rows: list[dict]):
    QUERY = """
    INSERT INTO chunks (
    document_id,
    user_id,
    tenant_id,
    content,
    content_hash,
    char_count,
    chunk_index
)
VALUES (
    %(document_id)s,
    %(user_id)s,
    %(tenant_id)s,
    %(content)s,
    %(content_hash)s,
    %(char_count)s,
    %(chunk_index)s
)
"""

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.executemany(QUERY, rows)
            await conn.commit()


async def get_chunks_by_document_id(
    document_id: UUID,
    user_id: UUID,
    tenant_id: UUID,
):
    QUERY = """
        SELECT *
        FROM chunks
        WHERE document_id = %s
          AND tenant_id = %s
          AND user_id = %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                QUERY,
                (document_id, tenant_id, user_id),
            )

            return await cur.fetchall()


async def fetch_chunks_by_chunk_ids(
    chunk_ids: list[UUID],
    user_id: UUID,
    tenant_id: UUID,
):
    QUERY = """
        SELECT *
        FROM chunks
        WHERE chunk_id = ANY(%s)
          AND tenant_id = %s
          AND user_id = %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                QUERY,
                (chunk_ids, tenant_id, user_id),
            )

            return await cur.fetchall()
