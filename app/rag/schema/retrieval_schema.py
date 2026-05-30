from pydantic import BaseModel, StrictStr
from typing import List, Optional

from uuid import UUID
from datetime import datetime


class QueryRequestSchema(BaseModel):
    content: StrictStr
    document_ids: Optional[List[UUID]] = None

    class Config:
        extra = "forbid"


class QuerySchema(BaseModel):
    content: StrictStr  # strings are allowed,
    tenant_id: UUID
    user_id: UUID
    # document_id: UUID


class QueryRecord(BaseModel):
    content: StrictStr  # strings are allowed,
    query_id: UUID
    tenant_id: UUID
    user_id: UUID
    created_at: datetime
    # document_id: UUID


class RetrievalRow(BaseModel):
    tenant_id: UUID
    user_id: UUID
    query_id: UUID
    content: str
    chunk_id: UUID
    document_id: UUID
    vector_score: float

class RetrievalBody(BaseModel):
    tenant_id: UUID
    user_id: UUID
    query_id: UUID
    chunk_id: UUID
    document_id: UUID
    vector_score: float

class RetrievalResponse(BaseModel):
    query: str
    context: list[RetrievalRow]
    reranked_chunks: bool


class RerankedChunkRow(BaseModel):
    query_id: UUID
    retrieved_chunk_id: UUID
    chunk_id: UUID
    user_id: UUID
    tenant_id: UUID
    document_id: UUID
    reranked_score: float


class RerankedChunkList(BaseModel):
    chunks: List[RerankedChunkRow]


class RerankedRow(BaseModel):
    tenant_id: UUID
    user_id: UUID
    query_id: UUID
    content:StrictStr
    chunk_id: UUID
    document_id: UUID
    reranked_score: float


class RerankedResponse(BaseModel):
    query: str
    context: list[RerankedRow]
    reranked_chunks: bool
