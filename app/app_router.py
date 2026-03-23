from app.rag.router.rag import rag_router
from app.document.router.document_router import document_router
from app.auth.auth_router import auth_router
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(rag_router)
app_router.include_router(auth_router)
app_router.include_router(document_router)