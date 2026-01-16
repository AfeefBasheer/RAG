from app.rag.text_splitter.chunks_validator import validate_chunks

def embed_the_chunks(chunks:list)->list:
    chunks = validate_chunks(chunks)
    #actual embedding here
    return chunks