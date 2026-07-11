from app.database.postgres import pool
from uuid import UUID
from psycopg.types.json import Json

async def create_job(job_type: str, document_id: UUID, user_id: UUID, tenant_id: UUID):

    QUERY = """
        SELECT create_job(%s, %s, %s, %s)
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                QUERY,
                (
                    job_type,
                    document_id,
                    user_id,
                    tenant_id,
                ),
            )

            result = await cur.fetchone()
            await conn.commit()
            return result


async def fetch_embed_job():

    QUERY = """
        SELECT *
        FROM fetch_and_lock_embed_job()
    """
    async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(QUERY)
                result = await cur.fetchone()

    return result if result else None



async def fetch_general_job():
    QUERY = """
        SELECT *
        FROM fetch_and_lock_general_job()
    """
    
    async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(QUERY)
                result = await cur.fetchone()
                return result if result else None



async def update_job(
    status: str,
    job_id: UUID,
    errors: list | None = None,
    attempt: int = 3,
):
    QUERY = """
        UPDATE job_queue
        SET
            status = %s,
            error = %s,
            attempt = %s
        WHERE job_id = %s
        RETURNING *
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                QUERY,
                    (
                        status,
                        Json(errors),
                        attempt,
                        job_id,
                    ),
                )

            result = await cur.fetchone()
            await conn.commit()
            return result



async def get_job_by_job_id(
    job_id: UUID,
    user_id: UUID,
    tenant_id: UUID,
):
    QUERY = """
        SELECT
            status,
            error,
            document_id,
            job_type
        FROM job_queue
        WHERE job_id = %s
          AND user_id = %s
          AND tenant_id = %s
    """

    async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    QUERY,
                    (
                        job_id,
                        user_id,
                        tenant_id,
                    ),
                )
                
                return await cur.fetchone()
