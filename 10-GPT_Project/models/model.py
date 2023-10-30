from sqlalchemy import Integer, String, ForeignKey, Column, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Langage(Base):
    __tablename__ = 'langage'
    id_langage = Column(Integer, primary_key=True)
    langage = Column(String(55))

class TexteCode(Base):
    __tablename__ = 'texte_code'
    id = Column(Integer, primary_key=True)
    id_langage = Column(Integer, ForeignKey('langage.id_langage'))
    texte = Column(String(3000))
    code = Column(String(3000))
    langage = relationship("Langage")