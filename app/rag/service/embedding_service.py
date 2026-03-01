from app.rag.repository.ingestion_repository import create_embeddings,get_embeddings_count
from qdrant_client.models import PointStruct
from app.core.vector_normalizer import normalize


def insert_embeddings(collection_name,chunks,embeddings):
    if(len(chunks) != len(embeddings)):
        raise Exception(f"Chunk Length not equal to emebdding length")
    elif(len(chunks) == 0 or len(embeddings)==0): 
        print(len(chunks),len(embeddings))
        raise Exception("Empty chunks or embeddings")
    points = []
    for chunk,vector in zip(chunks,embeddings):
        points.append(
            PointStruct(
                id=chunk["chunk_id"],  # UUID is perfect
                vector=normalize(vector),
                payload={
                    "tenant_id": chunk["tenant_id"],
                    "document_id": chunk["document_id"],
                    "content_hash": chunk["content_hash"],
                    "chunk_index": chunk["chunk_index"],
                },
            )
        )
    
    response = create_embeddings(points,collection_name)
    return response

def check_embeddings(collection_name,document_id,chunk_length):
    result = get_embeddings_count(collection_name,document_id)
    if(result.count == chunk_length): return True
    return False