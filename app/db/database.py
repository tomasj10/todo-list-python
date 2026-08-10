from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

connect_args = {
    "check_same_thread": 
    False
}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)

def get_session():
        with Session(engine) as session: 
            yield session

SessionDep = Annotated[Session, Depends(get_session)]
