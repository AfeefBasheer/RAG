from app.database.postgres import supabase
from postgrest.exceptions import APIError
from app.document.schema.document_schema import DocumentRecord,DocumentStatus,Document
from uuid import UUID


def insert_document(document: DocumentRecord):
    try:
        return (
            supabase.table("documents")
            .insert(
                {
                    "source_type": document.source_type,
                    "content": document.content,
                    "content_hash": document.content_hash,
                    "status": document.status,
                }
            )
            .execute()
        )
    except APIError as error:
        print("Error at insert_document", error)
        raise


def get_document_by_content_hash(content_hash: str):
    try:
        return (
            supabase.table("documents")
            .select("*")
            .eq("content_hash", content_hash)
            .single()
            .execute()
        )
    except APIError as error:
        print("Error at get_document_by_content_hash", error)
        raise


def get_document_by_document_id(document_id: UUID):
    try:
        response =  (
            supabase.table("documents")
            .select("*")
            .eq("document_id", document_id)
            .single()
            .execute()
        ).data
        return Document(**response)
    except APIError as error:
        print("Error at get_document_by_document_id", error)
        raise


def update_document_status(document_id: UUID, status: DocumentStatus):
    try:
        return (
            supabase.table("documents")
            .update({"status": status})
            .eq("document_id", document_id)
            .execute()
        ).data
    except APIError as error:
        print("Error at update_document_status", error)
        raise
