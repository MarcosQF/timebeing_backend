import uuid
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import Select

from timebeing_backend.database import T_Session
from timebeing_backend.models.task import Task
from timebeing_backend.schemas.task import TaskCreate, TaskSoftUpdate

from ..logger import logger
from ..scheduler.jobs import schedule_notification


class CRUDTask:
    @staticmethod
    async def create_task(session: T_Session, task: TaskCreate, user_id: str):
        logger.info(f'Criando task {task.model_dump()} para usuário {user_id}')
        task_data = task.model_dump()
        task_data['user_id'] = user_id
        db_task = Task(**task_data)

        if task.due_date and task.notify_at:
            schedule_notification(
                task_title=task.title,
                due_date=task.due_date,
                notify_at=task.notify_at,
            )

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        return db_task

    @staticmethod
    async def list_tasks(session: T_Session, user_id: str):
        db_tasks = await session.scalars(Select(Task).where(Task.user_id == user_id))

        logger.info(f'Listou as tasks do usuário {user_id}')

        return db_tasks

    @staticmethod
    async def get_task_by_id(session: T_Session, task_id: uuid.UUID, user_id: str):
        db_task = await session.scalar(
            Select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

        if not db_task:
            logger.warning(f'Task {task_id} não encontrada para usuário {user_id}')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
            )
        logger.info(f'Consultou o item {task_id} do usuário {user_id}')

        return db_task

    @staticmethod
    async def delete_task(session: T_Session, task_id: uuid.UUID, user_id: str):
        logger.info(f'Deletando task {task_id} do usuário {user_id}')
        db_task = await session.scalar(
            Select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

        if not db_task:
            logger.warning(f'Task {task_id} não encontrada para usuário {user_id}')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
            )

        await session.delete(db_task)
        await session.commit()

    @staticmethod
    async def soft_update_task(
        session: T_Session, task_id: uuid.UUID, task: TaskSoftUpdate, user_id: str
    ):
        db_task = await session.scalar(
            Select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

        if not db_task:
            logger.warning(f'Task {task_id} não encontrada para usuário {user_id}')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
            )

        logger.info(f'Atualizando task {task_id} para {task.model_dump()} do usuário {user_id}')

        for key, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        return db_task

    @staticmethod
    async def list_subtasks(session: T_Session, task_id: uuid.UUID, user_id: str):
        db_task = await session.scalar(
            Select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

        if not db_task:
            logger.info(f'Subtasks da task {task_id} não foram encontradas para usuário {user_id}')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Parent task not found',
            )

        db_subtasks = await session.scalars(
            Select(Task).where(Task.parent_task_id == task_id, Task.user_id == user_id)
        )

        logger.info(f'Consultando subtasks da task {task_id} do usuário {user_id}')

        return db_subtasks
