from app.document.persistance.ingestion import fetch_document_by_document_id
from app.document.persistance.ingestion import insert_chunks
# from app.rag.adapters.vector_database.ingestion import store_embeddings
from app.rag.pipeline.ingestion import ingestion_pipeline



async def ingest_document(document_id)-> bool:
    document = fetch_document_by_document_id(document_id)
    if not document.status == "admitted": 
        return False #something like this..
    pipeline_response = await ingestion_pipeline(document)
    chunk_response = insert_chunks(pipeline_response.document_id,pipeline_response.chunks)
    # print(chunk_response)
    # update_document_status(chunk_response.document_id,"chunked")
    # embedding_response = store_embeddings(pipeline_response.embeddings)
    # update_document_status(embedding_response.document_id,"embedded")
    # return True
