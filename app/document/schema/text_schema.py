from typing import Literal
from pydantic import BaseModel, StrictStr, ConfigDict


class TextRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: StrictStr  # strings are allowed,
    source_type: Literal["text"] = "text"

class TextSchema(BaseModel):
    content: str
    source_type: str
