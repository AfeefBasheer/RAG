from fastapi import APIRouter
from app.rag.service.retrieval_service import retrieve_data
from app.rag.schema.retrieval_schema import QueryRequestSchema

retrieval_router = APIRouter()


@retrieval_router.post("/retrieve")
def ingest_endpoint(query:QueryRequestSchema):
    tenant_id = '00000000-0000-0000-0000-000000000001' #from jwt
    user_id = '10000000-0000-0000-0000-000000000000' #from jwt
    response = retrieve_data(query,user_id,tenant_id)
    return response
