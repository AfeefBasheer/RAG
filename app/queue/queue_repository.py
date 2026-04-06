from app.database.postgres import supabase
from postgrest.exceptions import APIError
from uuid import UUID


def create_job(job_type, document_id: UUID, user_id: UUID, tenant_id: UUID):
    try:
        return supabase.rpc(
            "create_job_if_not_active",
            {
                "p_job_type": job_type,
                "p_document_id": str(document_id),
                "p_user_id": str(user_id),
                "p_tenant_id": str(tenant_id),
            },
        ).execute()
    except APIError as error:
        print("Error at create_job", error)
        raise


def fetch_job():
    try:
        response = supabase.rpc("fetch_and_lock").execute()
        if response.data:
            return response.data[0]
        else:
            return None
    except APIError as error:
        print("Error at fetch_job", error)
        raise


def update_job(status, job_id: UUID, error_message: str = None, attempt=3):
    try:
        response = (
            supabase.table("job_queue")
            .update(
                {"status": status, "error_message": error_message, "attempt": attempt}
            )
            .eq("job_id", job_id)
            .execute()
        )
        return response
    except APIError as error:
        print("Error at update_job", error)
        raise


def get_job_by_job_id(job_id: UUID, user_id: UUID, tenant_id: UUID):
    try:
        response = (
            supabase.table("job_queue")
            .select("status,error_message,document_id,job_type")
            .eq("job_id", job_id)
            .eq("user_id", user_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
        return response.data
    except APIError as error:
        print("Error at fetching job", error)
        raise
