import uuid
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import Select

from timebeing_backend.database import T_Session
from timebeing_backend.models.project import Project
from timebeing_backend.schemas.project import (
    ProjectCreate,
    ProjectSoftUpdate,
)


class CRUDProject:
    @staticmethod
    async def create_project(session: T_Session, project: ProjectCreate):
        db_project = Project(**project.model_dump())

        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)

        return db_project

    @staticmethod
    async def get_project_by_id(session: T_Session, project_id: uuid.UUID):
        db_project = await session.scalar(
            Select(Project).where(Project.id == project_id)
        )

        if not db_project:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Project not found'
            )

        return db_project

    @staticmethod
    async def list_projects(session: T_Session):
        db_projects = await session.scalars(Select(Project))

        return db_projects

    @staticmethod
    async def delete_project(session: T_Session, project_id: uuid.UUID):
        db_project = await session.scalar(
            Select(Project).where(Project.id == project_id)
        )

        if not db_project:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Project not found'
            )

        await session.delete(db_project)
        await session.commit()

    @staticmethod
    async def soft_update_project(
        session: T_Session, project_id: uuid.UUID, project: ProjectSoftUpdate
    ):
        db_project = await session.scalar(
            Select(Project).where(Project.id == project_id)
        )

        if not db_project:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Project not found'
            )

        for key, value in project.model_dump(exclude_unset=True).items():
            setattr(db_project, key, value)

        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)

        return db_project
