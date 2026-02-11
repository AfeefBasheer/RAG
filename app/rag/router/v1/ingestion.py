from fastapi import APIRouter
from uuid import UUID
from app.rag.service.ingestion import ingest_document

ingestion_router = APIRouter()


@ingestion_router.post("/ingest/{document_id}")
async def ingest_endpoint(document_id: UUID):
    response = await ingest_document(document_id)
    # return response
