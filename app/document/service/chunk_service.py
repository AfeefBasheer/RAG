from app.document.repository.chunk_repository import get_chunks_by_document_id, create_chunks
from uuid import UUID
from app.document.schema.chunk_schema import RawChunkRecord, ChunkRecord
from app.core.hash import hash_content


def fetch_chunks_by_document_id(document_id: UUID,tenant_id:UUID):
    return get_chunks_by_document_id(document_id,tenant_id)


def insert_chunks(document_id: UUID, raw_chunks: list[RawChunkRecord],tenant_id:UUID):
    chunks: list[ChunkRecord] = []

    for raw_chunk in raw_chunks:
        content_hash = hash_content(raw_chunk.content)

        chunk = ChunkRecord(
            document_id=document_id,
            tenant_id = tenant_id,
            content=raw_chunk.content,
            content_hash=content_hash,
            char_count=raw_chunk.char_count,
            chunk_index=raw_chunk.chunk_index
        )

        chunks.append(chunk)
    rows = [chunk.model_dump(mode="json") for chunk in chunks]


    return create_chunks(rows)
