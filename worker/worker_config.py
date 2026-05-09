from app.rag.service.ingestion_service import chunk_document, embed_document
from app.document.service.document_service import remove_document_record

MAX_ATTEMPT = 3

GENERAL_JOB_HANDLER = {
    "chunk_document": chunk_document,
    "delete_document": remove_document_record,
}

EMBEDDING_JOB_HANDLER= {
    "embed_document": embed_document,
}