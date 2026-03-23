from app.rag.repository.ingestion_repository import create_embeddings,get_embeddings_count
from qdrant_client.models import PointStruct
from app.core.vector_normalizer import normalize
from uuid import UUID


def insert_embeddings(collection_name:str,chunks,embeddings:list,user_id:UUID,tenant_id:UUID):
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
                    "document_id": chunk["document_id"],
                    "user_id":user_id,
                    "tenant_id":tenant_id,
                    "chunk_index": chunk["chunk_index"],
                },
            )
        )
    
    response = create_embeddings(points,collection_name)
    return response

def check_embeddings(chunk_length:int,collection_name:str,document_id:UUID,user_id:UUID,tenant_id:UUID):
    result = get_embeddings_count(collection_name,document_id,user_id,tenant_id)
    if(result.count == chunk_length): return True
    return False