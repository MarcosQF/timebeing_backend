import uuid
from http import HTTPStatus

from fastapi import APIRouter

from timebeing_backend.auth_middleware import CurrentUserId
from timebeing_backend.schemas.habit import Message

from ..cruds.task import CRUDTask
from ..database import T_Session
from ..schemas.task import TaskCreate, TaskList, TaskPublic, TaskSoftUpdate

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('/', status_code=HTTPStatus.OK, response_model=TaskList)
async def list_tasks(session: T_Session, user_id: CurrentUserId):
    db_tasks = await CRUDTask.list_tasks(session=session, user_id=user_id)

    return {'tasks': db_tasks}


@router.get('/{task_id}', status_code=HTTPStatus.OK, response_model=TaskPublic)
async def get_task_by_id(session: T_Session, task_id: uuid.UUID, user_id: CurrentUserId):
    db_task = await CRUDTask.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    return db_task


@router.get(
    '/{task_id}/subtasks', status_code=HTTPStatus.OK, response_model=TaskList
)
async def list_subtasks(session: T_Session, task_id: uuid.UUID, user_id: CurrentUserId):
    db_subtasks = await CRUDTask.list_subtasks(
        session=session, task_id=task_id, user_id=user_id
    )

    return {'tasks': db_subtasks}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TaskPublic)
async def create_task(session: T_Session, task: TaskCreate, user_id: CurrentUserId):
    db_task = await CRUDTask.create_task(session=session, task=task, user_id=user_id)

    return db_task


@router.delete('/{task_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_task(session: T_Session, task_id: uuid.UUID, user_id: CurrentUserId):
    await CRUDTask.delete_task(session=session, task_id=task_id, user_id=user_id)

    return {'message': 'Task has been deleted succesfully'}


@router.patch(
    '/{task_id}', status_code=HTTPStatus.OK, response_model=TaskPublic
)
async def soft_update_task(
    session: T_Session, task_id: uuid.UUID, task: TaskSoftUpdate, user_id: CurrentUserId
):
    db_task = await CRUDTask.soft_update_task(
        session=session, task_id=task_id, task=task, user_id=user_id
    )

    return db_task
