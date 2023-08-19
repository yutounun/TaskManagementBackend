from fastapi import APIRouter
from src.endpoints import task, project, user

router = APIRouter()
router.include_router(task.router)
router.include_router(project.router)
router.include_router(user.router)

# This file calls every apis under src/endpoints
