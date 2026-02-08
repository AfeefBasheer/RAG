from app.document.router.v1.text import text_router
from fastapi import APIRouter

document_router = APIRouter()
document_router.include_router(text_router)
