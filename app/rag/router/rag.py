from fastapi import APIRouter
from app.rag.router.v1.health import health_router
from app.rag.router.v1.ingestion import ingestion_router
from app.rag.router.v1.retrieval import retrieval_router

rag_router = APIRouter()
rag_router.include_router(health_router)
rag_router.include_router(retrieval_router)
rag_router.include_router(ingestion_router)
