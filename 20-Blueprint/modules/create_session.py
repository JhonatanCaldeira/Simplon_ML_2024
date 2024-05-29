from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model_blog import Base
import os

def create_db(name="base_de_donnees", path="database"):
    database = path+"/"+name
    if os.path.exists("{}.db".format(database)):
        engine = create_engine("sqlite:///{}.db".format(database))
    else:
        engine = create_engine("sqlite:///{}.db".format(database))
        Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session
