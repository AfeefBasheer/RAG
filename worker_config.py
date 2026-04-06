from app.rag.service.ingestion_service import ingest_document

MAX_ATTEMPT = 3
JOB_HANDLER = {"ingestion": ingest_document}