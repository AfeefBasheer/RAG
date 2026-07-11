from fastapi import APIRouter
from app.auth.auth_service import login_user
from app.auth.auth_schema import UserLoginRequestSchema

auth_router = APIRouter()

@auth_router.post('/login')
async def login_user_endpoint(login_schema:UserLoginRequestSchema):
    response = await login_user(login_schema)
    return response