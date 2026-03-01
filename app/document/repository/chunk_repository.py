from app.database.postgres import supabase
from postgrest.exceptions import APIError
from uuid import UUID


def create_chunks(rows: list[dict]):
    try:
        response = supabase.table("chunks").insert(rows).execute()
        return response.data
    except APIError as error:
        print("Error at create_chunks", error)
        raise


def get_chunks_by_document_id(document_id: UUID):
    try:
        response = (
            supabase.table("chunks")
            .select("*")
            .eq("document_id", document_id)
            .execute()
        )
        return response.data
    except APIError as error:
        print("Error at get_chunks_by_document_id", error)
        raise
