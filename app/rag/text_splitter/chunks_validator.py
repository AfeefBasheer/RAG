from app.rag.core.string_guard import require_str
from app.rag.embedder.config import MAX_CHUNK_CHARS_V1


def validate_chunks(chunks: list):
    validated = []
    for item in chunks:
        item = require_str(item, name="chunk_validator")
        if len(item) > MAX_CHUNK_CHARS_V1:
            raise ValueError(
                f"Chunk size greater than expected, expected size {MAX_CHUNK_CHARS_V1}, "
                f"received size {len(item)}, in chunks_validator."
            )
        validated.append(item)
    return validated