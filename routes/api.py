from fastapi import APIRouter
from src.endpoints import task

router = APIRouter()
router.include_router(task.router)

# This file calls every apis under src/endpoints
