from app.rag.router.rag import rag_router
from app.document.router.document import document_router
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(rag_router)
app_router.include_router(document_router)