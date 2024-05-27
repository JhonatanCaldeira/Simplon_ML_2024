from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model_blog import Base
import os


def create_db(name="base_de_donnees"):
    if os.path.exists("{}.db".format(name)):
        engine = create_engine("sqlite:///{}.db".format(name))
    else:
        engine = create_engine("sqlite:///{}.db".format(name))
        Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session
