from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from timebeing_backend.routers import habit, project, task

router = APIRouter(prefix='/api/v1')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

router.include_router(habit.router)
router.include_router(task.router)
router.include_router(project.router)

app.include_router(router)
