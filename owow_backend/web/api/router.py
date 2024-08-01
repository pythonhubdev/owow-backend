from fastapi import APIRouter

from owow_backend.web.api.docs import docs_router
from owow_backend.web.api.file import file_router
from owow_backend.web.api.monitoring import health_router
from owow_backend.web.api.user import user_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(docs_router)
api_router.include_router(file_router)
api_router.include_router(user_router)
