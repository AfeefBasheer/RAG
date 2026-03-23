from pydantic import BaseModel, StrictStr
from uuid import UUID
from datetime import datetime


class QueryRequestSchema(BaseModel):
    content: StrictStr

    class Config:
        extra = "forbid"


class QuerySchema(BaseModel):
    content: StrictStr  # strings are allowed,
    tenant_id: UUID
    user_id:UUID
    # document_id: UUID


class QueryRecord(BaseModel):
    content: StrictStr  # strings are allowed,
    query_id: UUID
    tenant_id:UUID
    user_id:UUID
    created_at: datetime
    # document_id: UUID


class RetrievalRow(BaseModel):
    tenant_id:UUID
    user_id:UUID
    content: StrictStr  # strings are allowed,
    query_id: UUID
    content_hash: str
    chunk_id: UUID
    document_id: UUID
    vector_score: float


class RetrievalRowRecord(BaseModel):
    query_id: UUID
    user_id:UUID
    content_hash: str
    tenant_id:UUID
    chunk_id: UUID
    document_id: UUID
    vector_score: float
    created_at: datetime


class RetrievedChunksRecord(BaseModel):
    rows: list[RetrievalRowRecord]


class RetrievalResponse(BaseModel):
    query: str
    context: list[RetrievalRow]
