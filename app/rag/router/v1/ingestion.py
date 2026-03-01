from fastapi import APIRouter
from uuid import UUID
from app.rag.service.ingestion_service import ingest_document

ingestion_router = APIRouter()


@ingestion_router.post("/ingest/{document_id}")
def ingest_endpoint(document_id: UUID):
    response = ingest_document(document_id)
    return response
