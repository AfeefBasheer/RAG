from app.rag.components.text_splitter.chunks_validator import validate_chunks
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

async def embed_the_chunks(chunks: list) -> list:
    chunks = validate_chunks(chunks)
    embedded_data = model.encode(chunks, normalize_embeddings=True,device = "cpu")
    return embedded_data
