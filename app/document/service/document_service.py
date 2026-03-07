from app.document.schema.text_schema import TextSchema
from app.document.schema.document_schema import DocumentRecord
from app.document.repository.document_repository import (
    insert_document,
    get_document_by_document_id,
    update_document_status
)
from app.core.hash import hash_content
from uuid import UUID


def admit_text(text: TextSchema,tenant_id: UUID):
    content_hash = hash_content(text.content)
    document_record = DocumentRecord(
        tenant_id = tenant_id,
        content_hash=content_hash,
        content=text.content,
        source_type="text",
        status="admitted",
    )

    response = insert_document(document_record)
    return response

def fetch_document_by_document_id(document_id:UUID,tenant_id:UUID):
    response = get_document_by_document_id(document_id,tenant_id)
    return response


def mark_document_chunked(document_id:UUID,tenant_id:UUID):
    return update_document_status(document_id, "chunked",tenant_id)

def mark_document_embedded(document_id:UUID,tenant_id:UUID):
    return update_document_status(document_id, "embedded",tenant_id)
