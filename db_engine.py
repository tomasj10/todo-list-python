from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "database.db"
SQLITE_DATABASE_URL = f"sqlite:///{sqlite_file_name}"

connect_args = {
    "check_same_thread": 
    False
}

engine = create_engine(SQLITE_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close() 

def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)

def get_session():
        with Session(engine) as session: 
            yield session

SessionDep = Annotated[Session, Depends(get_session)]
