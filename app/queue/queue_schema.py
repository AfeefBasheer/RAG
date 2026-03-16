from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

class JobRecord(BaseModel):
    document_id:Optional[UUID]
    job_id:UUID
    tenant_id:Optional[UUID]
    user_id:Optional[UUID]
    job_type:str
    status:str
    created_at:datetime
    updated_at:datetime
    attempt:int
    payload:Optional[Dict[str, Any]]
    error_message:Optional[str]