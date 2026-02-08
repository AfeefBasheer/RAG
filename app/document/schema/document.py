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
