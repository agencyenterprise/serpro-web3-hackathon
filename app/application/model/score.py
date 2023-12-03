from sqlalchemy import Column, String, Float
from app.application.model.db import Base


class ScoreModel(Base):
    __tablename__ = "score"
    address = Column(String, nullable=False)
    score = Column(Float, nullable=False)
