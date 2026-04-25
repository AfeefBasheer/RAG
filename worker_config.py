from app.rag.service.ingestion_service import ingest_document
from app.document.service.document_service import remove_document_record

MAX_ATTEMPT = 3

JOB_HANDLER = {"ingestion": ingest_document, "delete_document": remove_document_record}
