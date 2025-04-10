from fastapi import FastAPI
# from app.api.v1.routes import router as api_router
from app.api.v1.api import router as api_router

app = FastAPI(title="MirTech API")

app.include_router(api_router, prefix="/api/v1")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
