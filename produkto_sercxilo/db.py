from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = (
    'psycopg2+{db_url}'.format(db_url=environ.get('DATABASE_URL'))
) if environ.get('DATABASE_URL') else 'sqlite:///foo.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
