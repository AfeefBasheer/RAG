from app.document.repository.ingestion import get_document_by_document_id, create_chunks
from postgrest.exceptions import APIError
from app.core.hash import hash_text
from app.document.schema.document import ChunkRow
from app.document.schema.document import DocumentRecord


def fetch_document_by_document_id(document_id) -> DocumentRecord:
    try:
        response = get_document_by_document_id(document_id)
        return DocumentRecord(**response.data)
    except APIError:
        raise


# All chunk content must originate from identity-normalized document text.
# Chunk hashing must never re-normalize.

def insert_chunks(document_id, chunks) -> list:
    try:
        chunk_rows: list[ChunkRow] = []

        for raw_chunk in chunks:
            text = raw_chunk.content  # already normalized
            text_hash = hash_text(text)

            chunk_rows.append(
                ChunkRow(
                    document_id=document_id,
                    content=text,
                    content_hash=text_hash,
                    token_count=raw_chunk.char_count,
                    chunk_index=raw_chunk.chunk_index,
                )
            )

        # 🔑 serialize ONCE at the boundary
        rows = [row.model_dump(mode="json") for row in chunk_rows]

        response = create_chunks(rows)
        return response

    except APIError:
        raise
