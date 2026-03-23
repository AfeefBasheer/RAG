from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Literal
from uuid import UUID


class UserLoginRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str


class UserRecord(BaseModel):
    user_id: UUID
    password_hash: str
    tenant_id : UUID
    user_role : Literal["user"]

class UserBody(BaseModel):
    user_id : UUID
    tenant_id : UUID
    user_role : Literal["user"]
