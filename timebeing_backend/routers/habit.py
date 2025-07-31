import uuid
from http import HTTPStatus

from fastapi import APIRouter

from timebeing_backend.auth_middleware import CurrentUserId

from ..cruds.habit import CRUDHabit
from ..database import T_Session
from ..schemas.habit import (
    HabitCreate,
    HabitList,
    HabitPublic,
    HabitSoftUpdate,
    Message,
)

router = APIRouter(prefix='/habits', tags=['habits'])


@router.get('/', status_code=HTTPStatus.OK, response_model=HabitList)
async def list_habits(session: T_Session, user_id: CurrentUserId):
    all_habits = await CRUDHabit.list_habits(session=session, user_id=user_id)

    return {'habits': all_habits}


@router.get(
    '/{habit_id}', status_code=HTTPStatus.OK, response_model=HabitPublic
)
async def get_habit_by_id(session: T_Session, habit_id: uuid.UUID, user_id: CurrentUserId):
    db_habit = await CRUDHabit.get_habit(session=session, habit_id=habit_id, user_id=user_id)

    return db_habit


@router.delete(
    '/{habit_id}', status_code=HTTPStatus.OK, response_model=Message
)
async def delete_habit(session: T_Session, habit_id: uuid.UUID, user_id: CurrentUserId):
    await CRUDHabit.delete_habit(session=session, habit_id=habit_id, user_id=user_id)

    return {'message': 'Habit has been deleted successfully'}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=HabitPublic)
async def create_habit(session: T_Session, habit: HabitCreate, user_id: CurrentUserId):
    db_habit = await CRUDHabit.create_habit(session=session, habit=habit, user_id=user_id)

    return db_habit


@router.patch(
    '/{habit_id}', status_code=HTTPStatus.OK, response_model=HabitPublic
)
async def update_habit(
    session: T_Session, habit: HabitSoftUpdate, habit_id: uuid.UUID, user_id: CurrentUserId
):
    db_habit = await CRUDHabit.patch_habit(
        session=session, habit=habit, habit_id=habit_id, user_id=user_id
    )

    return db_habit
