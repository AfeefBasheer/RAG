from app.core.string_guard import require_str
from app.rag.config.embedder_config import MAX_CHUNK_CHARS_V1, BATCH_SIZE_V1


def validate_chunks(chunks: list):
    validated = []
    if len(chunks) > BATCH_SIZE_V1:
        raise ValueError(
            f"Chunk batch size greater than expected, expected batch size {BATCH_SIZE_V1}, "
            f"received size {len(chunks)}, in chunks_validator."
        )
    for item in chunks:
        item = require_str(item, name="chunk_validator")
        if len(item) > MAX_CHUNK_CHARS_V1:
            raise ValueError(
                f"Chunk size greater than expected, expected size {MAX_CHUNK_CHARS_V1}, "
                f"received size {len(item)}, in chunks_validator."
            )
        validated.append(item)
    return validated
