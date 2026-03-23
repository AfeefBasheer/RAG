from app.database.postgres import supabase
from postgrest.exceptions import APIError


def get_user_by_email(email:str):
    try:
        response = (
        supabase.table("users")
        .select("user_id, email, password_hash,tenant_id")
        .eq("email",email)
        .execute()
    )
        if response.data:
            return response.data[0]
        else: return None
    except APIError as error:
        print('error occured at get_user_by_email ',error)
        raise