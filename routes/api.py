from fastapi import APIRouter
from src.endpoints import task, project

router = APIRouter()
router.include_router(task.router)
router.include_router(project.router)

# This file calls every apis under src/endpoints
