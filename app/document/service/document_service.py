from app.document.schema.text_schema import TextSchema
from app.document.schema.document_schema import DocumentRecord
from app.document.repository.document_repository import (
    insert_document,
    get_document_by_document_id,
    update_document_status
)
from app.core.hash import hash_content
from uuid import UUID


def admit_text(text: TextSchema):
    content_hash = hash_content(text.content)
    document_record = DocumentRecord(
        content_hash=content_hash,
        content=text.content,
        source_type="text",
        status="admitted",
    )

    response = insert_document(document_record)
    return response

def fetch_document_by_document_id(document_id:UUID):
    response = get_document_by_document_id(document_id)
    return response


def mark_document_chunked(document_id):
    return update_document_status(document_id, "chunked")

def mark_document_embedded(document_id):
    return update_document_status(document_id, "embedded")
