from fastapi import APIRouter, FastAPI

from timebeing_backend.routers import habit, project, task

router = APIRouter(prefix='/api/v1')
app = FastAPI()

router.include_router(habit.router)
router.include_router(task.router)
router.include_router(project.router)

app.include_router(router)
