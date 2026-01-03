from fastapi import APIRouter

health_router = APIRouter()

@health_router.get('/health')
def show_health():
    return "the server is Healthy"