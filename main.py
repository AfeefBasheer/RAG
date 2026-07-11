from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.app_router import app_router
from app.database.postgres import pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INFO:     CONNECTED TO POSTGRESQL")

    await pool.open()

    try:
        yield

    finally:
        print("INFO:    CLOSING POSTGRESQL POOL")
        await pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(app_router)