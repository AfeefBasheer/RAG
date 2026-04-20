from qdrant_client.models import Filter, FieldCondition, MatchValue,FilterSelector
from app.database.vector_db import qdrant_client
from uuid import UUID

def create_embeddings(points, collection_name:str):
    response = qdrant_client.upsert(
        collection_name=collection_name,
        points=points,
    )
    return response


def get_embeddings_count(collection_name:str, document_id:UUID, user_id:UUID, tenant_id:UUID):
    result = qdrant_client.count(
        collection_name=collection_name,
        count_filter=Filter(
            must=[
                FieldCondition(
                    key="document_id", match=MatchValue(value=str(document_id))
                ),
                FieldCondition(key="tenant_id", match=MatchValue(value=str(tenant_id))),
                FieldCondition(key="user_id", match=MatchValue(value=str(user_id))),
            ]
        ),
    )
    return result


def delete_points_by_document_id(collection_name: str, document_id: UUID, user_id: UUID, tenant_id: UUID):
    response = qdrant_client.delete(
        collection_name=collection_name,
        points_selector=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(key="document_id", match=MatchValue(value=str(document_id))),
                    FieldCondition(key="tenant_id", match=MatchValue(value=str(tenant_id))),
                    FieldCondition(key="user_id", match=MatchValue(value=str(user_id))),
                ]
            )
        ),
    )
    return response
