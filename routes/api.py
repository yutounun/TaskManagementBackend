from fastapi import APIRouter
from src.endpoints import auth, task, project

router = APIRouter()
router.include_router(task.router)
router.include_router(project.router)
router.include_router(auth.router)

# This file calls every apis under src/endpoints
