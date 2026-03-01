from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("QDRANT_ENDPOINT")
QDRANT_KEY = os.getenv("QDRANT_KEY")

qdrant_client = QdrantClient(
    url=API_URL,
    api_key=QDRANT_KEY,
)


def create_embeddings(points,collection_name):

    response = qdrant_client.upsert(
        collection_name=collection_name,
        points=points,
    )
    return response

def get_embeddings_count(collection_name,document_id):
    result = qdrant_client.count(
        collection_name = collection_name,
        count_filter=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=str(document_id))
                ),
                # FieldCondition(
                #     key="tenant_id",
                #     match=MatchValue(value=str(tenant_id))
                # ),
            ]
        )
    )
    return result
