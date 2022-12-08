from sqlalchemy import Column, String, Text

from .base import BaseInvestModel


MAX_LEN_OF_PROJECT_NAME = 100


class CharityProject(BaseInvestModel):
    name = Column(String(MAX_LEN_OF_PROJECT_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)
