from fastapi import APIRouter

from app.api.v1 import articles, events, health, predict

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(articles.router)
api_router.include_router(events.router)
api_router.include_router(predict.router)
