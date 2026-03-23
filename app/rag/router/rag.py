from fastapi import APIRouter
from app.rag.router.v1.ingestion_router import ingestion_router
from app.rag.router.v1.retrieval_router import retrieval_router

rag_router = APIRouter()
rag_router.include_router(retrieval_router)
rag_router.include_router(ingestion_router)
