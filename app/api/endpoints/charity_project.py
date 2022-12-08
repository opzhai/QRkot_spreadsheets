from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate,
                                check_charity_project_exists,
                                check_project_name,
                                check_new_sum,
                                check_closed_project,
                                check_project_with_invested_sum)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.donation_services import donation_process
from app.models import Donation


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    check_project_name(charity_project.name)
    await check_name_duplicate(charity_project.name, session)
    commit_action = False
    charity_project = await charity_project_crud.create(
        charity_project, session, commit_action
    )
    changed_obects = await donation_process(
        charity_project, Donation, session
    )
    for obj in changed_obects:
        session.add(obj)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_closed_project(charity_project.id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_new_sum(project_id, obj_in.full_amount, session)
    charity_project_updated = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    charity_project_reinvested = await donation_process(
        charity_project_updated, Donation, session
    )
    for obj in charity_project_reinvested:
        session.add(obj)
    await session.commit()
    await session.refresh(charity_project_updated)
    return charity_project_updated


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_project_with_invested_sum(project_id, session)
    await check_closed_project(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
