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
    if overlap_size >= chunk_size:
        raise ValueError("overlap must be smaller than chunk size")

    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+|(?<=[.!?])(?=[A-Z])", text)

    chunks = []
    current_chunk = []

    def join_chunk(chunk_list):
        return " ".join(chunk_list).strip()

    def chunk_length(chunk_list):
        if not chunk_list:
            return 0
        return sum(len(s) for s in chunk_list) + (len(chunk_list) - 1)

    def trim_overlap(chunk_list):
        """Keep only last N characters worth of sentences"""
        total = 0
        new_chunk = []

        for sentence in reversed(chunk_list):
            sentence_len = len(sentence)
            extra_space = 1 if new_chunk else 0

            if total + extra_space + sentence_len > overlap_size:
                break

            new_chunk.insert(0, sentence)
            total += extra_space + sentence_len

        return new_chunk

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        sentence_len = len(sentence)

        # 🔴 Handle very large single sentence
        if sentence_len > chunk_size:
            if current_chunk:
                joined = join_chunk(current_chunk)
                chunks.append(
                    RawChunkRecord(len(chunks), joined, len(joined))
                )
                current_chunk = []

            for i in range(0, sentence_len, chunk_size):
                part = sentence[i:i + chunk_size]
                chunks.append(
                    RawChunkRecord(len(chunks), part, len(part))
                )
            continue

        # Try adding sentence
        temp_chunk = current_chunk + [sentence]
        if chunk_length(temp_chunk) <= chunk_size:
            current_chunk.append(sentence)
        else:
            # flush current chunk
            joined = join_chunk(current_chunk)

            # 🔴 HARD SAFETY CHECK
            if len(joined) > chunk_size:
                raise RuntimeError(
                    f"Chunk overflow bug: {len(joined)} > {chunk_size}"
                )

            chunks.append(
                RawChunkRecord(len(chunks), joined, len(joined))
            )

            # apply character-based overlap
            current_chunk = trim_overlap(current_chunk)

            # retry adding sentence after overlap
            temp_chunk = current_chunk + [sentence]
            if chunk_length(temp_chunk) > chunk_size:
                # edge case: sentence still doesn't fit → force new chunk
                chunks.append(
                    RawChunkRecord(len(chunks), sentence, len(sentence))
                )
                current_chunk = []
            else:
                current_chunk.append(sentence)

    # Final flush
    if current_chunk:
        joined = join_chunk(current_chunk)

        if len(joined) > chunk_size:
            raise RuntimeError(
                f"Final chunk overflow bug: {len(joined)} > {chunk_size}"
            )

        chunks.append(
            RawChunkRecord(len(chunks), joined, len(joined))
        )

    return chunks