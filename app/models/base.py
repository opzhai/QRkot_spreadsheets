from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean, CheckConstraint

from app.core.db import Base


class BaseInvestModel(Base):

    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount >= invested_amount'),
        CheckConstraint('full_amount > 0'),
    )

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)
