import uuid
from http import HTTPStatus

from fastapi import APIRouter

from timebeing_backend.auth_middleware import CurrentUserId
from timebeing_backend.cruds.project import CRUDProject
from timebeing_backend.database import T_Session
from timebeing_backend.models.project import ProjectStatus
from timebeing_backend.schemas.habit import Message

from ..schemas.project import (
    ProjectCreate,
    ProjectList,
    ProjectPublic,
    ProjectSoftUpdate,
    ProjectStatusOptions,
    ProjectTasks,
)

router = APIRouter(prefix='/projects', tags=['projects'])


@router.get(
    '/status-options',
    status_code=HTTPStatus.OK,
    response_model=ProjectStatusOptions,
)
async def get_project_status_options():
    """Get available project status options with labels and descriptions."""

    status_options = [
        {
            'value': ProjectStatus.criado.value,
            'label': 'Planejamento',
            'description': 'Projeto em fase de planejamento',
        },
        {
            'value': ProjectStatus.andamento.value,
            'label': 'Em Andamento',
            'description': 'Projeto ativo em desenvolvimento',
        },
        {
            'value': ProjectStatus.concluido.value,
            'label': 'Concluído',
            'description': 'Projeto finalizado com sucesso',
        },
    ]

    return {'status_options': status_options}


@router.get(
    '/{project_id}', status_code=HTTPStatus.OK, response_model=ProjectPublic
)
async def get_project_by_id(session: T_Session, project_id: uuid.UUID, user_id: CurrentUserId):
    db_project = await CRUDProject.get_project_by_id(
        session=session, project_id=project_id, user_id=user_id
    )

    return db_project


@router.get('/', status_code=HTTPStatus.OK, response_model=ProjectList)
async def list_projects(session: T_Session, user_id: CurrentUserId):
    db_projects = await CRUDProject.list_projects(session=session, user_id=user_id)

    return {'projects': db_projects}


@router.get(
    '/{project_id}/tasks',
    status_code=HTTPStatus.OK,
    response_model=ProjectTasks,
)
async def list_tasks(session: T_Session, project_id: uuid.UUID, user_id: CurrentUserId):
    db_tasks = await CRUDProject.list_tasks(
        session=session, project_id=project_id, user_id=user_id
    )

    return {'tasks': db_tasks}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ProjectPublic)
async def create_project(session: T_Session, project: ProjectCreate, user_id: CurrentUserId):
    db_project = await CRUDProject.create_project(
        session=session, project=project, user_id=user_id
    )

    return db_project


@router.delete(
    '/{project_id}', status_code=HTTPStatus.OK, response_model=Message
)
async def delete_project(session: T_Session, project_id: uuid.UUID, user_id: CurrentUserId):
    await CRUDProject.delete_project(session=session, project_id=project_id, user_id=user_id)

    return {'message': 'Project has been deleted succesfully'}


@router.patch(
    '/{project_id}', status_code=HTTPStatus.OK, response_model=ProjectPublic
)
async def soft_update_project(
    session: T_Session, project_id: uuid.UUID, project: ProjectSoftUpdate, user_id: CurrentUserId
):
    db_project = await CRUDProject.soft_update_project(
        session=session, project_id=project_id, project=project, user_id=user_id
    )

    return db_project
