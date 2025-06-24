from fastapi import APIRouter, FastAPI

from timebeing_backend.routers import habit

router = APIRouter(
    prefix='/api/v1'
)
app = FastAPI()

router.include_router(habit.router)

app.include_router(router)
