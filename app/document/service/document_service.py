from app.document.schema.text_schema import TextSchema
from app.document.schema.document_schema import DocumentRecord
from app.rag.service.embedding_service import remove_points
from app.rag.config.embedder_config import COLLECTION_NAME
from app.document.repository.document_repository import (
    insert_document,
    get_document_by_document_id,
    update_document_status,
    delete_document_by_document_id,
)
from app.core.hash import hash_content
from uuid import UUID


def admit_text(text: TextSchema, user_id: UUID, tenant_id: UUID):
    content_hash = hash_content(text.content)
    document_record = DocumentRecord(
        tenant_id=tenant_id,
        user_id=user_id,
        content_hash=content_hash,
        content=text.content,
        source_type="text",
        status="admitted",
    )

    response = insert_document(document_record)
    return response


def fetch_document_by_document_id(document_id: UUID, user_id: UUID, tenant_id: UUID):
    response = get_document_by_document_id(document_id, user_id, tenant_id)
    return response


def mark_document_chunked(document_id: UUID, user_id: UUID, tenant_id: UUID):
    return update_document_status("chunked", document_id, user_id, tenant_id)


def mark_document_embedded(document_id: UUID, user_id: UUID, tenant_id: UUID):
    return update_document_status("embedded", document_id, user_id, tenant_id)


def remove_document_record(document_id: UUID, user_id: UUID, tenant_id: UUID):

    error = None
    point_delete_response = None
    document_delete_response = None

    try:
        point_delete_response = remove_points(
            COLLECTION_NAME, document_id, user_id, tenant_id
        )
    except Exception as e:
        print("Remove Document failed at vector db")
        error = str(e)

    try:
        document_delete_response = delete_document_by_document_id(
            document_id, user_id, tenant_id
        )
    except Exception as e:
        print("Remove Document failed at Postgres db")
        error = str(e)

    if error:
        raise Exception(error)

    return {
        "vector_db_response": point_delete_response,
        "postgres_db_response": document_delete_response,
    }
