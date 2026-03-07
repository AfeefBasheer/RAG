from fastapi import APIRouter
from uuid import UUID
from app.rag.service.ingestion_service import ingest_document

ingestion_router = APIRouter()


@ingestion_router.post("/ingest/{document_id}")
def ingest_endpoint(document_id: UUID):
    tenant_id = '00000000-0000-0000-0000-000000000001' # from jwt
    response = ingest_document(document_id,tenant_id)
    return response
