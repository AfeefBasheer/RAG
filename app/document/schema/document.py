from typing import Literal
from pydantic import BaseModel, StrictStr
from uuid import UUID

class textRequestSchema(BaseModel):
    text: StrictStr  # strings are allowed,
    source_type: Literal["text"] = ("text",)

    class Config:
        extra = "forbid"


class DocumentRecord(BaseModel):
    text: StrictStr
    document_id: UUID
    source_type: Literal["text"] = "text"
    status: Literal["admitted","failed", "chunked", "embedded"]
    content_hash: StrictStr

class RawDocument(BaseModel):
    text: StrictStr
    document_id: UUID
    source_type: Literal["text"] = "text"
    status: Literal["admitted","failed", "chunked", "embedded"]

class IngestedDocumentRecord(BaseModel):
    chunks: list
    embeddings: list
    document_id:UUID

class RawChunkObject(BaseModel):
    chunk_index:int
    content: StrictStr
    char_count: int

class ChunkRow(BaseModel):
    content:StrictStr
    token_count:int
    document_id:UUID
    chunk_index:int
    content_hash:StrictStr