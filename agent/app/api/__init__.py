from fastapi import APIRouter
from .agent import router as agent_router

router = APIRouter()

router.include_router(agent_router)
