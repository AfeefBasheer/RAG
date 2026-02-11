from app.rag.components.embedder.text_embedder import embed_the_chunks
from app.rag.components.text_splitter.chunker import chunk_data_by_chars
from app.rag.config.text_splitter import CHUNK_SIZE_v1,OVERLAP_SIZE_v1
from app.document.schema.document import DocumentRecord,IngestedDocumentRecord

async def ingestion_pipeline(document:DocumentRecord)-> IngestedDocumentRecord:
    chunked_data = chunk_data_by_chars(document.text,CHUNK_SIZE_v1,OVERLAP_SIZE_v1)    
    embedded_data =await embed_the_chunks(chunked_data)
    response = IngestedDocumentRecord(
        document_id=document.document_id,
        chunks=chunked_data,
        embeddings=embedded_data,
    )
    return response
