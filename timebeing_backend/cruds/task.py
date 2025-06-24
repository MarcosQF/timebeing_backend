import uuid
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import Select

from timebeing_backend.database import T_Session
from timebeing_backend.models.task import Task
from timebeing_backend.schemas.task import TaskCreate, TaskSoftUpdate


class CRUDTask:
    @staticmethod
    async def create_task(session: T_Session, task: TaskCreate):
        db_task = Task(**task.model_dump())

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        return db_task

    @staticmethod
    async def list_tasks(session: T_Session):
        db_tasks = await session.scalars(Select(Task))

        return db_tasks

    @staticmethod
    async def get_task_by_id(session: T_Session, task_id: uuid.UUID):
        db_task = await session.scalar(Select(Task).where(Task.id == task_id))

        if not db_task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Task not found'
            )

        return db_task

    @staticmethod
    async def delete_task(session: T_Session, task_id: uuid.UUID):
        db_task = await session.scalar(Select(Task).where(Task.id == task_id))

        if not db_task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Task not found'
            )

        await session.delete(db_task)
        await session.commit()

    @staticmethod
    async def soft_update_task(
        session: T_Session, task_id: uuid.UUID, task: TaskSoftUpdate
    ):
        db_task = await session.scalar(Select(Task).where(Task.id == task_id))

        if not db_task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Task not found'
            )

        for key, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        return db_task
