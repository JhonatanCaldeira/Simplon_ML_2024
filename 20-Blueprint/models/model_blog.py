from sqlalchemy import (
    Column,
    Integer,
    Text,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ModelBlog(Base):
    __tablename__ = "model_blog"
    id = Column(Integer, primary_key=True)
    comment = Column(Text)
