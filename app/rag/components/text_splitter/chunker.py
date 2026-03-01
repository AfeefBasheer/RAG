from app.core.string_guard import require_str
from app.document.schema.chunk_schema import RawChunkRecord


def chunk_data_by_chars(text: str, chunk_size: int, overlap_size: int):
    text = require_str(text, name="split_data")

    if len(text) == 0:
        raise ValueError("text must not be empty")

    if overlap_size <= 0 or overlap_size >= chunk_size:
        raise ValueError("overlap_size must be > 0 and < chunk_size")

    step = chunk_size - overlap_size
    text_chunks = []

    start = 0
    n = len(text)
    index = 0
    while start < n:
        end = min(start + chunk_size, n)
        chunk = RawChunkRecord(chunk_index = index,content=text[start:end], char_count=len(text[start:end]))
        index = index+1
        text_chunks.append(chunk)

        if end == n:
            break

        start += step

    return text_chunks
