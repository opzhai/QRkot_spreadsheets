from datetime import datetime
from typing import Set

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.base import BaseInvestModel


def change_obj(obj: BaseInvestModel, min_value: int) -> BaseInvestModel:
    obj.invested_amount += min_value
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()
    return obj


async def donation_process(
    obj_in: BaseInvestModel,
    model_db: BaseInvestModel,
    session: AsyncSession
):
    crudbase = CRUDBase(model_db)
    items_not_fully_invested = await crudbase.get_multi_not_fully_invested(
        session
    )
    res = []
    for db_item in items_not_fully_invested:
        if obj_in.invested_amount is None:
            obj_in.invested_amount = 0
        min_value = min(obj_in.full_amount - obj_in.invested_amount,
                        db_item.full_amount - db_item.invested_amount)
        change_obj(obj_in, min_value)
        change_obj(db_item, min_value)
        res.append(db_item)
        if obj_in.fully_invested:
            break
    return res


def donation_process_produce(
    obj_in: BaseInvestModel,
    obj_db: BaseInvestModel
) -> Set[BaseInvestModel]:
    if obj_in.invested_amount is None:
        obj_in.invested_amount = 0
    obj_in_difference = obj_in.full_amount - obj_in.invested_amount
    obj_db_difference = obj_db.full_amount - obj_db.invested_amount
    min_value = min(obj_in_difference, obj_db_difference)
    obj_in = change_obj(obj_in, min_value)
    obj_db = change_obj(obj_db, min_value)
    return obj_in, obj_db
