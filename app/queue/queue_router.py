from fastapi import APIRouter,Depends
from app.queue.queue_service import get_job
from app.auth.auth_dependency import get_current_user
from uuid import UUID
from app.auth.auth_schema import UserBody


queue_router = APIRouter()

@queue_router.get('/job/{job_id}')
def fetch_job_endpoint(job_id:UUID,user: UserBody = Depends(get_current_user)):
    response = get_job(job_id,user.user_id,user.tenant_id)
    return response