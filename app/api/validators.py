# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.models.charity_project import MAX_LEN_OF_PROJECT_NAME


def check_project_name(project_name: str) -> None:
    if (
        project_name is None or
        len(project_name) == 0 or
        len(project_name) > MAX_LEN_OF_PROJECT_NAME
    ):
        raise HTTPException(
            status_code=422,
            detail='Название проекта обязательно. '
            'Названием не может быть пусая строка. '
            'Название не может длиннее {num} символов.'.format(
                num=MAX_LEN_OF_PROJECT_NAME
            )
        )


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(charity_project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_new_sum(
    charity_project_id: int,
    new_sum: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(charity_project_id, session)
    if new_sum < project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Требуемая сумма не может быть меньше уже внесенной суммы!'
        )
    return project


async def check_closed_project(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(charity_project_id, session)
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    return project


async def check_project_with_invested_sum(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(charity_project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project
