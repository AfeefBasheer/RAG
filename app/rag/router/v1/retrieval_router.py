from fastapi import APIRouter, Depends
from app.auth.auth_dependency import get_current_user
from app.auth.auth_schema import UserBody
from app.rag.service.retrieval_service import retrieve_data
from app.rag.schema.retrieval_schema import QueryRequestSchema
from uuid import UUID

retrieval_router = APIRouter()


@retrieval_router.post("/retrieve")
async def ingest_endpoint(
    query: QueryRequestSchema, user: UserBody = Depends(get_current_user)
):
    response = await retrieve_data(query, user.user_id, user.tenant_id)
    return response
