from app.database.postgres import pool

async def get_user_by_email(email: str):

    query = """
        SELECT
            user_id,
            email,
            password_hash,
            tenant_id
        FROM users
        WHERE email = %s
    """

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (email,))

            user = await cur.fetchone()
            return user