# from app.rag.components.input_normalizer.text import normalize_data
# from app.rag.components.embedder.text_embedder import embed_the_chunks
# from app.rag.components.text_splitter.chunker import chunk_data
# from app.rag.config.text_splitter import CHUNK_SIZE_v1,OVERLAP_SIZE_v1

# def ingestion_pipeline(ingestion_data):
#     text = normalize_data(ingestion_data.text)
#     chunked_data = chunk_data(text,CHUNK_SIZE_v1,OVERLAP_SIZE_v1)
#     embedded_data = embed_the_chunks(chunked_data)
#     response = {embedded_data,chunked_data,text}
#     return response
