from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject
from app.models import User
from app.schemas.donation import (DonationBase, DonationAllUsersDB,
                                  DonationUserDB, DonationUserCreate)
from app.services.donation_services import donation_process


router = APIRouter()


@router.post('/',
             response_model=DonationUserCreate,
             response_model_exclude={'user_id'},
             response_model_exclude_none=True
             )
async def create_donation(
        donation: DonationBase,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    commit_action = False
    new_donation = await donation_crud.create(
        donation, session, commit_action, user
    )
    changed_obects = await donation_process(
        new_donation, CharityProject, session
    )
    for obj in changed_obects:
        session.add(obj)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get('/', response_model=list[DonationAllUsersDB],
            dependencies=[Depends(current_superuser)],
            )
async def get_all_users_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get('/my',
            response_model=list[DonationUserDB],
            response_model_exclude={'user_id'},
            )
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    user_donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return user_donations
