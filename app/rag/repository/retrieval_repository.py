from app.database.vector_db import qdrant_client
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.database.postgres import supabase
from postgrest.exceptions import APIError
from app.rag.schema.retrieval_schema import QuerySchema
from uuid import UUID


def insert_query(query: QuerySchema):
    try:
        response = (
            supabase.table("query")
            .insert(
                {
                    "content": query.content,
                    "user_id": str(query.user_id),
                    "tenant_id": str(query.tenant_id),
                }
            )
            .execute()
        )
        return response.data[0]
    except APIError as error:
        print("Error at insert query", error)


def insert_retrieved_chunks(retrieved_data):
    try:
        rows = [row.model_dump(mode="json") for row in retrieved_data]

        response = supabase.table("retrieved_chunks").insert(rows).execute()

        return response.data

    except APIError as error:
        print("Error at insert retrieved data", error)
        raise


def retrieve_embeddings(
    query_vector: str, COLLECTION_NAME: str, TOP_K: int, user_id: UUID, tenant_id: UUID
):
    response = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=TOP_K,
        query_filter=Filter(
            must=[
                FieldCondition(key="tenant_id", match=MatchValue(value=str(tenant_id))),
                FieldCondition(key="user_id", match=MatchValue(value=str(user_id))),
            ]
        ),
    )
    return response.points
