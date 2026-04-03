from app.core.string_guard import require_str
from app.rag.config.embedder_config import MAX_CHUNK_CHARS_V1, BATCH_SIZE_V1


def validate_chunks(chunks: list):
    validated_batches = []
    batches = batch_chunks(chunks)

    for batch in batches:
        validated_batch = []
        for item in batch:
            item = require_str(item, name="chunk_validator")
            if len(item) > MAX_CHUNK_CHARS_V1:
                raise ValueError(
                    f"Chunk size greater than expected, expected size {MAX_CHUNK_CHARS_V1}, "
                    f"received size {len(item)}, in chunks_validator. The chunk is '{item[:200]}'"
                )
            validated_batch.append(item)
        validated_batches.append(validated_batch)
    return validated_batches


def batch_chunks(chunks):
    batches = []
    count = 0

    while count < len(chunks):
        batches.append(chunks[count : (count + BATCH_SIZE_V1)])
        count = count + BATCH_SIZE_V1
    return batches
