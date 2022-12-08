from typing import Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt


CURRENT_TIME = (datetime.now()).isoformat(timespec='minutes')


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationUserCreate(DonationBase):
    id: int
    comment: Optional[str]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationUserDB(DonationUserCreate):
    create_date: Optional[datetime]


class DonationAllUsersDB(DonationUserDB):
    user_id: int
    full_amount: PositiveInt
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
