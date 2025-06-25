import uuid
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import Select

from timebeing_backend.database import T_Session
from timebeing_backend.models.habit import Habit
from timebeing_backend.schemas.habit import HabitCreate, HabitSoftUpdate


class CRUDHabit:
    @staticmethod
    async def create_habit(session: T_Session, habit: HabitCreate):
        db_habit = Habit(**habit.model_dump())

        session.add(db_habit)
        await session.commit()
        await session.refresh(db_habit)

        return db_habit

    @staticmethod
    async def list_habits(session: T_Session):
        db_habits = await session.scalars(Select(Habit))

        return db_habits

    @staticmethod
    async def get_habit(session: T_Session, habit_id: uuid.UUID):
        db_habit = await session.scalar(
            Select(Habit).where(Habit.id == habit_id)
        )

        if not db_habit:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='habit not found'
            )

        return db_habit

    @staticmethod
    async def delete_habit(session: T_Session, habit_id: uuid.UUID):
        db_habit = await session.scalar(
            Select(Habit).where(Habit.id == habit_id)
        )

        if not db_habit:
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
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='habit not found'
            )

        for key, value in habit.model_dump(exclude_unset=True).items():
            setattr(db_habit, key, value)

        session.add(db_habit)
        await session.commit()
        await session.refresh(db_habit)

        return db_habit
