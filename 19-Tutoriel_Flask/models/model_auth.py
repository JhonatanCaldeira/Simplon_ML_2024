from sqlalchemy import (
    Column,
    Integer,
    Text,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ModelAuth(Base):
    __tablename__ = "model_auth"
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    email = Column(Text)
    password = Column(Text)
