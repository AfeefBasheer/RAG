from app.core.string_guard import require_str
from app.document.schema.chunk_schema import RawChunkRecord
import re


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
        chunk = RawChunkRecord(
            chunk_index=index, content=text[start:end], char_count=len(text[start:end])
        )
        index = index + 1
        text_chunks.append(chunk)

        if end == n:
            break

        start += step

    return text_chunks


def chunk_data_by_sentence(text: str, chunk_size: int, overlap_size: int):
    if not text:
        raise ValueError("text cannot be empty")
    if chunk_size <= 0:
        raise ValueError("invalid chunk size")
    if overlap_size < 0:
        raise ValueError("invalid overlap size")

    sentences = re.split(
        r"(?<=[.!?])\s+|(?<=[.!?])(?=[A-Z])", text
    )  # split the text into array of sentences on the basis of space . ! ?

    chunks = []
    current_chunk = []
    current_len = 0

    for sentence in sentences:
        sentence_len = len(sentence)

        # handle oversized sentence
        if sentence_len > chunk_size:
            if current_chunk:
                joined = " ".join(
                    current_chunk
                )  # join the array into a single string seperated by space.
                chunks.append(
                    RawChunkRecord(
                        chunk_index=len(chunks),
                        content=joined,  # appending into the chunks array.
                        char_count=len(joined),
                    )
                )
                current_chunk = []
                current_len = 0

            for i in range(0, sentence_len, chunk_size):
                part = sentence[i : i + chunk_size].strip()
                chunks.append(
                    RawChunkRecord( 
                        chunk_index=len(chunks), #handle if a sentence is larger max_chunK_size
                        content=part,
                        char_count=len(part),
                    )
                )
            continue

        extra_space = 1 if current_chunk else 0

        if current_len + extra_space + sentence_len > chunk_size:
            joined = " ".join(current_chunk)
            chunks.append(
                RawChunkRecord(
                    chunk_index=len(chunks), 
                    content=joined, # handle extraspace
                    char_count=len(joined),
                )
            )

            # overlap
            current_chunk = current_chunk[-overlap_size:]
            current_len = sum(len(s) for s in current_chunk) + max(
                len(current_chunk) - 1, 0
            )

        current_chunk.append(sentence)
        current_len += extra_space + sentence_len

    if current_chunk:
        joined = " ".join(current_chunk)
        chunks.append(
            RawChunkRecord(
                chunk_index=len(chunks), #last sentence
                content=joined,
                char_count=len(joined),
            )
        )

    return chunks
