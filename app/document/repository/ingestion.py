from app.database.postgres import supabase


def get_document_by_document_id(document_id):
    return (
        supabase.table("documents")
        .select("*")
        .eq("document_id", document_id)
        .single()
        .execute()
    )

def create_chunks(rows:list[dict]):
        return (
        supabase
        .table("chunks")
        .insert(rows)
        .execute()
    )