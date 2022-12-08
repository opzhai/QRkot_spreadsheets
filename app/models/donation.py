from sqlalchemy import ForeignKey, Column, Text, Integer

from .base import BaseInvestModel


class Donation(BaseInvestModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
