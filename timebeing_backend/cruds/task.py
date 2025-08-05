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
        logger.info(
            'Criando task %s para usuário %s', task.model_dump(), user_id
        )
        db_task = task.model_dump()
        db_task['user_id'] = user_id
        db_task = Task(**db_task)

        if task.due_date and task.notify_at:
            await schedule_notification(
                task_title=task.title,
                due_date=task.due_date,
                notify_at=task.notify_at,
                user_id=user_id,
            )

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        return db_task

    @staticmethod
    async def list_tasks(session: T_Session, user_id: str):
        db_tasks = await session.scalars(
            Select(Task).where(Task.user_id == user_id)
        )

        logger.info('Listou as tasks do usuário %s', user_id)

        return db_tasks

    @staticmethod
    async def get_task_by_id(
        session: T_Session, task_id: uuid.UUID, user_id: str
    ):
        db_task = await session.scalar(
            Select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

        if not db_task:
            logger.warning(
                'Task %s não encontrada para usuário %s', task_id, user_id
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
            )
        logger.info('Consultou o item %s do usuário %s', task_id, user_id)

        return db_task

    @staticmethod
    async def delete_task(
        session: T_Session, task_id: uuid.UUID, user_id: str
    ):
        logger.info('Deletando task %s do usuário %s', task_id, user_id)
        db_task = await session.scalar(
            Select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

        if not db_task:
            logger.warning(
                'Task %s não encontrada para usuário %s', task_id, user_id
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
            )

        await session.delete(db_task)
        await session.commit()

    @staticmethod
    async def soft_update_task(
        session: T_Session,
        task_id: uuid.UUID,
        task: TaskSoftUpdate,
        user_id: str,
    ):
        db_task: Task | None = await session.scalar(
            Select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

        if not db_task:
            logger.warning(
                'Task %s não encontrada para usuário %s', task_id, user_id
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
            )

        title_task = db_task.title

        logger.info(
            'Atualizando task %s para %s do usuário %s',
            task_id,
            task.model_dump(),
            user_id,
        )

        for key, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)

        if db_task.due_date and db_task.notify_at:
            await schedule_notification(
                task_title=title_task,
                due_date=db_task.due_date,
                notify_at=db_task.notify_at,
                user_id=user_id,
            )

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        return db_task

    @staticmethod
    async def list_subtasks(
        session: T_Session, task_id: uuid.UUID, user_id: str
    ):
        db_task = await session.scalar(
            Select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

        if not db_task:
            logger.info(
                'Subtasks da task %s não foram encontradas para usuário %s',
                task_id,
                user_id,
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Parent task not found',
            )

        db_subtasks = await session.scalars(
            Select(Task).where(
                Task.parent_task_id == task_id, Task.user_id == user_id
            )
        )

        logger.info(
            'Consultando subtasks da task %s do usuário %s',
            task_id,
            user_id,
        )

        return db_subtasks
