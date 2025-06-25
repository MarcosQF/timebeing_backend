import uuid
from http import HTTPStatus

from fastapi import APIRouter

from timebeing_backend.cruds.project import CRUDProject
from timebeing_backend.database import T_Session
from timebeing_backend.schemas.habit import Message

from ..schemas.project import (
    ProjectCreate,
    ProjectList,
    ProjectPublic,
    ProjectSoftUpdate,
    ProjectTasks,
)

router = APIRouter(prefix='/projects', tags=['projects'])


@router.get(
    '/{project_id}', status_code=HTTPStatus.OK, response_model=ProjectPublic
)
async def get_project_by_id(session: T_Session, project_id: uuid.UUID):
    db_project = await CRUDProject.get_project_by_id(
        session=session, project_id=project_id
    )

    return db_project


@router.get('/', status_code=HTTPStatus.OK, response_model=ProjectList)
async def list_projects(session: T_Session):
    db_projects = await CRUDProject.list_projects(session=session)

    return {'projects': db_projects}


@router.get(
    '/{project_id}/tasks',
    status_code=HTTPStatus.OK,
    response_model=ProjectTasks,
)
async def list_tasks(session: T_Session, project_id: uuid.UUID):
    db_tasks = await CRUDProject.list_tasks(
        session=session, project_id=project_id
    )

    return {'tasks': db_tasks}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ProjectPublic)
async def create_project(session: T_Session, project: ProjectCreate):
    db_project = await CRUDProject.create_project(
        session=session, project=project
    )

    return db_project


@router.delete(
    '/{project_id}', status_code=HTTPStatus.OK, response_model=Message
)
async def delete_project(session: T_Session, project_id: uuid.UUID):
    await CRUDProject.delete_project(session=session, project_id=project_id)

    return {'message': 'Project has been deleted succesfully'}


@router.patch(
    '/{project_id}', status_code=HTTPStatus.OK, response_model=ProjectPublic
)
async def soft_update_project(
    session: T_Session, project_id: uuid.UUID, project: ProjectSoftUpdate
):
    db_project = await CRUDProject.soft_update_project(
        session=session, project_id=project_id, project=project
    )

    return db_project
