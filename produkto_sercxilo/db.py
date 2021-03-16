from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') 
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
