from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.database.vector_db import qdrant_client


def create_embeddings(points, collection_name):
    response = qdrant_client.upsert(
        collection_name=collection_name,
        points=points,
    )
    return response


def get_embeddings_count(collection_name, document_id, user_id, tenant_id):
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
