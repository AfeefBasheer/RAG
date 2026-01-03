from fastapi import APIRouter
from app.rag.router.v1.health import health_router

rag_router = APIRouter()
rag_router.include_router(health_router)