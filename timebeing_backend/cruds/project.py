import uuid
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import Select

from timebeing_backend.database import T_Session
from timebeing_backend.models.project import Project
from timebeing_backend.models.task import Task
from timebeing_backend.schemas.project import (
    ProjectCreate,
    ProjectSoftUpdate,
)

from ..logger import logger


class CRUDProject:
    @staticmethod
    async def create_project(
        session: T_Session, project: ProjectCreate, user_id: str
    ):
        logger.info(
            'Criando project %s para usuário %s',
            project.model_dump(), user_id
        )
        project_data = project.model_dump()
        project_data['user_id'] = user_id
        db_project = Project(**project_data)

        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)

        return db_project

    @staticmethod
    async def get_project_by_id(
        session: T_Session, project_id: uuid.UUID, user_id: str
    ):
        db_project = await session.scalar(
            Select(Project).where(
                Project.id == project_id, Project.user_id == user_id
            )
        )

        if not db_project:
            logger.warning(
                'Project %s não encontrado para usuário %s',
                project_id, user_id
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Project not found'
            )

        return db_project

    @staticmethod
    async def list_projects(session: T_Session, user_id: str):
        db_projects = await session.scalars(
            Select(Project).where(Project.user_id == user_id)
        )

        return db_projects

    @staticmethod
    async def delete_project(
        session: T_Session, project_id: uuid.UUID, user_id: str
    ):
        logger.info('Deletando project %s do usuário %s', project_id, user_id)
        db_project = await session.scalar(
            Select(Project).where(
                Project.id == project_id, Project.user_id == user_id
            )
        )

        if not db_project:
            logger.warning(
                'Project %s não encontrado para usuário %s',
                project_id, user_id
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Project not found'
            )

        await session.delete(db_project)
        await session.commit()

    @staticmethod
    async def soft_update_project(
        session: T_Session,
        project_id: uuid.UUID,
        project: ProjectSoftUpdate,
        user_id: str,
    ):
        db_project = await session.scalar(
            Select(Project).where(
                Project.id == project_id, Project.user_id == user_id
            )
        )

        if not db_project:
            logger.warning(
                'Project %s não encontrado para usuário %s',
                project_id, user_id
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Project not found'
            )

        logger.info(
            'Atualizando project %s para %s do usuário %s',
            project_id, project.model_dump(), user_id
        )

        for key, value in project.model_dump(exclude_unset=True).items():
            setattr(db_project, key, value)

        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)

        return db_project

    @staticmethod
    async def list_tasks(
        session: T_Session, project_id: uuid.UUID, user_id: str
    ):
        db_project = await session.scalar(
            Select(Project).where(
                Project.id == project_id, Project.user_id == user_id
            )
        )

        if not db_project:
            logger.warning(
                'Project %s não encontrado para usuário %s',
                project_id, user_id
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Project not found'
            )

        db_tasks = await session.scalars(
            Select(Task).where(
                Task.project_id == project_id, Task.user_id == user_id
            )
        )
        logger.info(
            'Consultando tasks do projeto %s do usuário %s',
            project_id, user_id
        )

        return db_tasks
