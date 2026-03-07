from enum import Enum
from pydantic import BaseModel, StrictStr
from typing import Literal
from uuid import UUID
from typing import Optional
from datetime import datetime

class DocumentStatus(str, Enum):
    ADMITTED = "admitted"
    CHUNKED = "chunked"
    EMBEDDED = "embedded"
    FAILED = "failed"


class DocumentRecord(BaseModel):
    content: StrictStr
    source_type: Literal["text"] = "text"
    status: DocumentStatus
    content_hash: StrictStr


class Document(BaseModel):
    document_id: UUID
    content: StrictStr
    source_type: Optional[str] = None
    status: DocumentStatus
    content_hash: StrictStr
    storage_path: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    request_id: Optional[str] = None
