from app.database.vector_db import qdrant_client
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny
from app.database.postgres import supabase
from postgrest.exceptions import APIError
from app.rag.schema.retrieval_schema import QuerySchema,RerankedChunkList
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


def insert_reranked_chunks(reranked_chunks: RerankedChunkList):
    try:
        rows = reranked_chunks.model_dump(mode="json")["chunks"]

        response = (
            supabase
            .table("reranked_chunks")
            .insert(rows)
            .execute()
        )

        return response.data

    except APIError as error:
        print("Error at insert reranked data", error)
        raise


def retrieve_embeddings(
    query_vector: str,
    COLLECTION_NAME: str,
    document_ids: list[UUID] | None,
    TOP_K_RETRIEVAL: int,
    user_id: UUID,
    tenant_id: UUID,
):
    must_condition = [
        FieldCondition(key="tenant_id", match=MatchValue(value=str(tenant_id))),
        FieldCondition(key="user_id", match=MatchValue(value=str(user_id))),
    ]
    if document_ids:
        must_condition.append(
            FieldCondition(
                key="document_id",
                match=MatchAny(any=[str(doc_id) for doc_id in document_ids]),
            )
        )

    response = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=TOP_K_RETRIEVAL,
        query_filter=Filter(must=must_condition),
    )
    return response.points



def retrieve_chunks_with_chunk_content_from_query_id(
    query_id: UUID,
    user_id: UUID,
    tenant_id: UUID,
):
    try:
        response = (
            supabase.table("retrieved_chunks")
            .select("""
        *,
        chunks (
            content
        )
        """)
            .eq("query_id",str(query_id))
            .eq("tenant_id", str(tenant_id))
            .eq("user_id", str(user_id))
            .execute()
        )

        return response.data
    except APIError as error:
        print("Error at fetching retreived data", error)
        raise
    
    
def retrieve_chunks_with_chunk_content(
    chunk_ids: list[UUID],
    user_id: UUID,
    tenant_id: UUID,
):

    try:
        response = (
            supabase.table("retrieved_chunks")
            .select("""
        *,
        chunks (
            content
        )
        """)
            .in_("chunk_id", [str(chunk_id) for chunk_id in chunk_ids])
            .eq("tenant_id", str(tenant_id))
            .eq("user_id", str(user_id))
            .execute()
        )

        return response.data
    except APIError as error:
        print("Error at fetching retreived data", error)
        raise


def fetch_top_retrieved_chunks(
    query_id: UUID,
    TOP_K: int,
    user_id: UUID,
    tenant_id: UUID,
):
    try:
        response = (
            supabase.table("retrieved_chunks")
            .select("""
            *,
            chunks (
                content
            )
            """)
            .eq("query_id", str(query_id))
            .eq("tenant_id", str(tenant_id))
            .eq("user_id", str(user_id))
            .order("vector_score", desc=True)
            .limit(int(TOP_K))
            .execute()
        )

        normalized_rows = []

        for row in response.data:
            normalized_rows.append({
                "query_id": row["query_id"],
                "chunk_id": row["chunk_id"],
                "document_id": row["document_id"],
                "tenant_id": row["tenant_id"],
                "user_id": row["user_id"],
                "vector_score": row["vector_score"],
                "content": row["chunks"]["content"],
            })

        return normalized_rows

    except APIError as error:
        print("Error at fetching top retrieved data", error)
        raise