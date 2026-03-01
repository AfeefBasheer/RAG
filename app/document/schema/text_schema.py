from typing import Literal
from pydantic import BaseModel, StrictStr


class TextRequestSchema(BaseModel):
    content: StrictStr  # strings are allowed,
    source_type: Literal["text"] = "text"

    class Config:
        extra = "forbid"


class TextSchema(BaseModel):
    content: str
    source_type: str
