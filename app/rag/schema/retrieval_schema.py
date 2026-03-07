
from pydantic import BaseModel, StrictStr
from uuid import UUID
from datetime import datetime


class QuerySchema(BaseModel):
    content: StrictStr  # strings are allowed,
    # document_id: UUID

    class Config:
        extra = "forbid"

class QueryRecord(BaseModel):
    content: StrictStr  # strings are allowed,
    query_id:UUID
    created_at: datetime
    # document_id: UUID

class RetrievalRow(BaseModel):
    content: StrictStr  # strings are allowed,
    query_id: UUID
    content_hash: str
    chunk_id:UUID
    document_id:UUID
    vector_score:float

class RetrievalRowRecord(BaseModel):
    content: StrictStr  # strings are allowed,
    query_id: UUID
    content_hash: str
    chunk_id:UUID
    document_id:UUID
    vector_score:float
    created_at:datetime


class RetrievedChunksRecord(BaseModel):
    rows: list[RetrievalRowRecord]

class RetrievalResponse(BaseModel):
    query: str
    context: list[RetrievalRow]