from fastapi import APIRouter
from app.rag.router.v1.health import health_router
from app.rag.router.v1.ingestion import ingestion_router

rag_router = APIRouter()
rag_router.include_router(health_router)
rag_router.include_router(ingestion_router)
