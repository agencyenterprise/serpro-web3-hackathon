from sqlalchemy import Column, String, Float
from api.application.model.db import Base


class ScoreModel(Base):
    __tablename__ = "score"
    address = Column(String, nullable=False, unique=True, index=True)
    score = Column(Float, nullable=False)
