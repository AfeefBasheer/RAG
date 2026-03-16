from fastapi import APIRouter
from uuid import UUID
from app.queue.queue_service import enqueue_ingestion_job

ingestion_router = APIRouter()


@ingestion_router.post("/ingest/{document_id}")
def ingest_endpoint(document_id: UUID):
    tenant_id = "00000000-0000-0000-0000-000000000001"  # from jwt
    user_id = "10000000-0000-0000-0000-000000000000"  # from jwt
    response = enqueue_ingestion_job(document_id, user_id, tenant_id)
    return response
