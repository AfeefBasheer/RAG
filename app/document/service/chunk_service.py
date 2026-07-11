from app.document.repository.chunk_repository import (
    get_chunks_by_document_id,
    create_chunks,
    fetch_chunks_by_chunk_ids
)
from uuid import UUID
from app.document.schema.chunk_schema import RawChunkRecord, ChunkRecord
from app.core.hash import hash_content


async def fetch_chunks_by_document_id(document_id: UUID, user_id: UUID, tenant_id: UUID):
    return await get_chunks_by_document_id(document_id, user_id, tenant_id)


async def insert_chunks(
    raw_chunks: list[RawChunkRecord], document_id: UUID, user_id: UUID, tenant_id: UUID
):
    chunks: list[ChunkRecord] = []

    for raw_chunk in raw_chunks:
        content_hash = hash_content(raw_chunk.content)

        chunk = ChunkRecord(
            document_id=document_id,
            user_id=user_id,
            tenant_id=tenant_id,
            content=raw_chunk.content,
            content_hash=content_hash,
            char_count=raw_chunk.char_count,
            chunk_index=raw_chunk.chunk_index,
        )

        chunks.append(chunk)
    rows = [chunk.model_dump(mode="json") for chunk in chunks]

    response = await create_chunks(rows)
    return response

async def retrieve_chunks(chunk_ids:list,user_id:UUID,tenant_id:UUID):
    response = await fetch_chunks_by_chunk_ids(chunk_ids,user_id,tenant_id)
    return response
