# from app.rag.adapters.database.ingestion import (
#     get_document_by_document_id,
#     store_chunks,
# )


# from app.rag.adapters.vector_database.ingestion import store_embeddings
# from app.rag.pipeline.ingestion import ingestion_pipeline



# async def ingest_document(document_id):
#     document = get_document_by_document_id(document_id)
#     pipeline_artifact = await ingestion_pipeline(document)
#     store_chunks(pipeline_artifact.chunks)
#     store_embeddings(pipeline_artifact.embeddings)
#     return True
