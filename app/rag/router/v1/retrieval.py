from fastapi import APIRouter
from app.rag.service.retrieval_service import retrieve_data
from app.rag.schema.retrieval_schema import QuerySchema

retrieval_router = APIRouter()


@retrieval_router.post("/retrieve")
def ingest_endpoint(query:QuerySchema):
    response = retrieve_data(query)
    return response
