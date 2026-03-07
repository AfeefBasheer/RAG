from app.document.schema.text_schema import TextRequestSchema
from app.document.service.document_service import admit_text
from fastapi import APIRouter

text_router = APIRouter()


@text_router.post("/text")
def register_text_endpoint(text: TextRequestSchema):
    tenant_id = '00000000-0000-0000-0000-000000000001' #from jwt
    response = admit_text(text,tenant_id)
    return response
