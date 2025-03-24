# Refered from
# https://flask.palletsprojects.com/en/stable/patterns/sqlalchemy/

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

USER = "root"
PASSWORD = "root"
URL = "127.0.0.1"
PORT = 3306
DB = "dublin_bikes"


connect_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URL}:{PORT}/{DB}"
engine = create_engine(connect_string, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models.user
    Base.metadata.create_all(bind=engine)

    return engine