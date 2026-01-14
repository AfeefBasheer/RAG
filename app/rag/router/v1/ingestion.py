from fastapi import APIRouter
from app.rag.schema.ingestion import IngestionDataSchema
from app.rag.pipeline.ingestion import ingest

ingestion_router = APIRouter()


@ingestion_router.post("/ingest")
def ingest_data(ingestion_data: IngestionDataSchema):
    response = ingest(ingestion_data)
    return response
