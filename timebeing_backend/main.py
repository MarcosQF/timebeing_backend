from fastapi import APIRouter, FastAPI

from timebeing_backend.routers import habit, task

router = APIRouter(
    prefix='/api/v1'
)
app = FastAPI()

router.include_router(habit.router)
router.include_router(task.router)

app.include_router(router)
