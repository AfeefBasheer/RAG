from fastapi import APIRouter, Depends
from app.auth.auth_dependency import get_current_user
from app.auth.auth_schema import UserBody
from uuid import UUID
from app.queue.queue_service import enqueue_ingestion_job

ingestion_router = APIRouter()


@ingestion_router.post("/ingest/{document_id}")
def ingest_endpoint(document_id: UUID, user: UserBody = Depends(get_current_user)):
    response = enqueue_ingestion_job(document_id, user.user_id, user.tenant_id)
    return response
