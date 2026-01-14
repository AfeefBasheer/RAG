from pydantic import BaseModel, StrictStr

class IngestionDataSchema(BaseModel):
    text: StrictStr #strings are allowed
