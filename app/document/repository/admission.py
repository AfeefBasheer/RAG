from app.database.postgres import supabase


def create_document(document):
    response = (
        supabase.table("documents")
        .insert(
            {
                "document_id": str(document.document_id),
                "source_type": document.source_type,
                "text": document.text,
                "content_hash": document.content_hash,
                "status": document.status,
            }
        )
        .execute()
    )
    return response


def get_document_by_content_hash(content_hash):
    return (
        supabase
        .table("documents")
        .select("*")
        .eq("content_hash", content_hash).single()
        .execute()
    )
