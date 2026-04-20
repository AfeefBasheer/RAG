from app.document.router.v1.text_router import text_router
from fastapi import APIRouter,Depends
from uuid import UUID
from app.auth.auth_dependency import get_current_user
from app.queue.queue_service import enqueue_document_deletion_job
from app.auth.auth_schema import UserBody

document_router = APIRouter()

@document_router.delete('/document/{document_id}')
def delete_document_endpoint(document_id: UUID,user:UserBody =Depends(get_current_user)):
    response= enqueue_document_deletion_job(document_id,user.user_id,user.tenant_id)
    return response
    
document_router.include_router(text_router)

