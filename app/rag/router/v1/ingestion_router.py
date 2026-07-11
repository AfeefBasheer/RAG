from fastapi import APIRouter, Depends
from app.auth.auth_dependency import get_current_user
from app.auth.auth_schema import UserBody
from uuid import UUID
from app.rag.service.ingestion_service import ingest_document

ingestion_router = APIRouter()


@ingestion_router.post("/ingest/{document_id}")
async def ingest_endpoint(document_id: UUID, user: UserBody = Depends(get_current_user)):
    response = await ingest_document(document_id,user.user_id,user.tenant_id)
    return response
