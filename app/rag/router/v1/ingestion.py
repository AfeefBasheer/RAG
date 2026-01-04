from fastapi import APIRouter
from app.rag.schema.ingestion import ingestion_data_schema

ingestion_router = APIRouter()

@ingestion_router.post('/ingest')
def ingest_data(ingestion_data:ingestion_data_schema):
    return ingestion_data.text