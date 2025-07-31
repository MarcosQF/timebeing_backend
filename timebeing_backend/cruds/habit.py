import uuid
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import Select

from timebeing_backend.database import T_Session
from timebeing_backend.models.habit import Habit
from timebeing_backend.schemas.habit import HabitCreate, HabitSoftUpdate

from ..logger import logger


class CRUDHabit:
    @staticmethod
    async def create_habit(session: T_Session, habit: HabitCreate, user_id: str):
        logger.info(f'Criando habit {habit.model_dump()} para usuário {user_id}')
        habit_data = habit.model_dump()
        habit_data['user_id'] = user_id
        db_habit = Habit(**habit_data)

        session.add(db_habit)
        await session.commit()
        await session.refresh(db_habit)

        return db_habit

    @staticmethod
    async def list_habits(session: T_Session, user_id: str):
        db_habits = await session.scalars(Select(Habit).where(Habit.user_id == user_id))

        logger.info(f'Listou os habits do usuário {user_id}')

        return db_habits

    @staticmethod
    async def get_habit(session: T_Session, habit_id: uuid.UUID, user_id: str):
        db_habit = await session.scalar(
            Select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        )

        if not db_habit:
            logger.warning(f'Habit {habit_id} não encontrado para usuário {user_id}')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='habit not found'
            )

        logger.info(f'Consultou o habit {habit_id} do usuário {user_id}')

        return db_habit

    @staticmethod
    async def delete_habit(session: T_Session, habit_id: uuid.UUID, user_id: str):
        logger.info(f'Deletando habit {habit_id} do usuário {user_id}')
        db_habit = await session.scalar(
            Select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        )

        if not db_habit:
            logger.warning(f'Habit {habit_id} não encontrado para usuário {user_id}')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='habit not found'
            )

        await session.delete(db_habit)
        await session.commit()

    @staticmethod
    async def patch_habit(
        session: T_Session, habit_id: uuid.UUID, habit: HabitSoftUpdate, user_id: str
    ):
        db_habit = await session.scalar(
            Select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        )

        if not db_habit:
            logger.warning(f'Habit {habit_id} não encontrado para usuário {user_id}')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='habit not found'
            )

        logger.info(f'Atualizando habit {habit_id} para {habit.model_dump()} do usuário {user_id}')

        for key, value in habit.model_dump(exclude_unset=True).items():
            setattr(db_habit, key, value)

        session.add(db_habit)
        await session.commit()
        await session.refresh(db_habit)

        return db_habit
