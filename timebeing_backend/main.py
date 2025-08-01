import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from timebeing_backend.routers import habit, project, task
from .logger import logger  # Import configured logger


@asynccontextmanager
async def lifespan(app):
    logger.info('Iniciando Aplicação')
    start_scheduler()
    yield
    logger.info('Encerrando Aplicação')
    stop_scheduler()


router = APIRouter(prefix='/api/v1')
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:8080',
        'http://localhost:5173',
        'http://localhost:5174',
        'https://internal-piglet-88.clerk.accounts.dev',
        'https://clerk.shared.lcl.dev',
        'https://*.clerk.accounts.dev',
        'https://*.clerk.com'
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

router.include_router(habit.router)
router.include_router(task.router)
router.include_router(project.router)

app.include_router(router)
