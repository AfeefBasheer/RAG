from app.database.vector_db import qdrant_client
from app.database.postgres import supabase
from postgrest.exceptions import APIError
from app.rag.schema.retrieval_schema import QueryRecord


def insert_query(query: str):
    try:
        response =  (
            supabase.table("query")
            .insert(
                {
                    "content": query,
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

        response = (
            supabase
            .table("retrieved_chunks")
            .insert(rows)
            .execute()
        )

        return response.data

    except APIError as error:
        print("Error at insert retrieved data", error)
        raise

def retrieve_chunks(query_vector, COLLECTION_NAME, TOP_K=5):
    response = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=TOP_K,
    )
    return response.points
