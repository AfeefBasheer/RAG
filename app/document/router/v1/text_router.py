from app.document.schema.text_schema import TextRequestSchema
from app.document.service.document_service import admit_text
from fastapi import APIRouter, Depends
from app.auth.auth_dependency import get_current_user
from app.auth.auth_schema import UserBody

text_router = APIRouter()


@text_router.post("/text")
def register_text_endpoint(
    text: TextRequestSchema, user: UserBody = Depends(get_current_user)
):
    response = admit_text(text, user.user_id, user.tenant_id)
    return response
