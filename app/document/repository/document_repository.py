from uuid import UUID

from app.database.postgres import pool
from app.document.schema.document_schema import (
    DocumentRecord,
    DocumentStatus,
)


async def insert_document(document: DocumentRecord):
    QUERY = """
        INSERT INTO documents (
            source_type,
            tenant_id,
            user_id,
            content,
            content_hash,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
    """

    values = (
        document.source_type,
        document.tenant_id,
        document.user_id,
        document.content,
        document.content_hash,
        document.status,
    )

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(QUERY, values)
            result = await cur.fetchone()
            await conn.commit()
            return result


async def get_document_by_content_hash(
    content_hash: str,
    user_id: UUID,
    tenant_id: UUID,
):
    QUERY = """
        SELECT *
        FROM documents
        WHERE content_hash = %s
          AND user_id = %s
          AND tenant_id = %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                QUERY,
                (content_hash, user_id, tenant_id),
            )
            return await cur.fetchone()


async def get_document_by_document_id(
    document_id: UUID,
    user_id: UUID,
    tenant_id: UUID,
):
    QUERY = """
        SELECT *
        FROM documents
        WHERE document_id = %s
          AND user_id = %s
          AND tenant_id = %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                QUERY,
                (document_id, user_id, tenant_id),
            )
            return await cur.fetchone()


async def update_document_status(
    status: DocumentStatus,
    document_id: UUID,
    user_id: UUID,
    tenant_id: UUID,
):
    QUERY = """
        UPDATE documents
        SET status = %s
        WHERE document_id = %s
          AND user_id = %s
          AND tenant_id = %s
        RETURNING *
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                QUERY,
                (status, document_id, user_id, tenant_id),
            )
            result = await cur.fetchone()
            await conn.commit()
            return result


async def delete_document_by_document_id(
    document_id: UUID,
    user_id: UUID,
    tenant_id: UUID,
):
    QUERY = """
        DELETE FROM documents
        WHERE document_id = %s
          AND user_id = %s
          AND tenant_id = %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                QUERY,
                (document_id, user_id, tenant_id),
            )
            await conn.commit()