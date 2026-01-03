from fastapi import FastAPI
from app.app_router import app_router
app = FastAPI()

app.include_router(app_router)
