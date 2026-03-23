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


def get_chunks_by_document_id(document_id: UUID, user_id: UUID, tenant_id: UUID):
    try:
        response = (
            supabase.table("chunks")
            .select("*")
            .eq("document_id", document_id)
            .eq("user_id", user_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
        return response.data
    except APIError as error:
        print("Error at get_chunks_by_document_id", error)
        raise


def fetch_chunks_by_chunk_ids(chunk_ids:list, user_id:UUID, tenant_id:UUID):
    try:
        response = supabase.table("chunks").select("*").in_("chunk_id", chunk_ids).eq(
            "tenant_id", str(tenant_id)
        ).eq("user_id", str(user_id)).execute()
        return response.data
    except APIError as error:
        print("Error at retrive_chunks", error)
        raise
