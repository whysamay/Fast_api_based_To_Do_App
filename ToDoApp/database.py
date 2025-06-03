from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sampaw20@localhost/TodoApplicationDatabase"

# used to create a locaton for database for fast api, our db
# will be in this directory

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# connect args to dfine connection, sql library allows only one thread to interact w db
# but in fastapi, we may have multiple thread interacting w the sql
# SessionLocal connect to our engine and autocommit and autoflush doesnt happen in db
# declarative base is db object that we can interact w later on

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()