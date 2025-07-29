import logging
import uuid
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import Select

from timebeing_backend.database import T_Session
from timebeing_backend.models.habit import Habit
from timebeing_backend.schemas.habit import HabitCreate, HabitSoftUpdate

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class CRUDHabit:
    @staticmethod
    async def create_habit(session: T_Session, habit: HabitCreate):
        logger.info(f'Criando habit {habit.model_dump()}')
        db_habit = Habit(**habit.model_dump())

        session.add(db_habit)
        await session.commit()
        await session.refresh(db_habit)

        return db_habit

    @staticmethod
    async def list_habits(session: T_Session):
        db_habits = await session.scalars(Select(Habit))

        logger.info('listou os habits')

        return db_habits

    @staticmethod
    async def get_habit(session: T_Session, habit_id: uuid.UUID):
        db_habit = await session.scalar(
            Select(Habit).where(Habit.id == habit_id)
        )

        if not db_habit:
            logger.warning(f'Habit {habit_id} não encontrado')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='habit not found'
            )

        logger.info(f'Consultou o habit {habit_id}')

        return db_habit

    @staticmethod
    async def delete_habit(session: T_Session, habit_id: uuid.UUID):
        logger.info(f'Deletando habit {habit_id}')
        db_habit = await session.scalar(
            Select(Habit).where(Habit.id == habit_id)
        )

        if not db_habit:
            logger.warning(f'Habit {habit_id} não encontrada')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='habit not found'
            )

        await session.delete(db_habit)
        await session.commit()

    @staticmethod
    async def patch_habit(
        session: T_Session, habit_id: uuid.UUID, habit: HabitSoftUpdate
    ):
        db_habit = await session.scalar(
            Select(Habit).where(Habit.id == habit_id)
        )

        if not db_habit:
            logger.warning(f'Habit {habit_id} não encontrada')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='habit not found'
            )

        logger.info(
            f'Atualizando habit {habit_id} para {habit.model_dump()}'
        )

        for key, value in habit.model_dump(exclude_unset=True).items():
            setattr(db_habit, key, value)

        session.add(db_habit)
        await session.commit()
        await session.refresh(db_habit)

        return db_habit
