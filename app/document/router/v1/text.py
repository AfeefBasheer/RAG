from app.document.schema.document import textRequestSchema
from app.document.service.admission import admit_text
from fastapi import APIRouter

text_router = APIRouter()


@text_router.post("/text")
async def register_text_endpoint(text: textRequestSchema):
    response = await admit_text(text)
    return response
