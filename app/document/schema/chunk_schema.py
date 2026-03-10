from pydantic import BaseModel, StrictStr
from uuid import UUID

class ChunkRecord(BaseModel):
    tenant_id:UUID
    user_id:UUID
    content: StrictStr
    char_count: int
    document_id: UUID
    chunk_index: int
    content_hash: StrictStr

class RawChunkRecord(BaseModel):
    content: StrictStr
    char_count: int
    chunk_index: int

