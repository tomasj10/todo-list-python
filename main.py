from fastapi import FastAPI, Query
from user import User

from sqlmodel import select 
from db_engine import create_db_and_tables, SessionDep
from typing import Annotated

app = FastAPI()


@app.get('/users')
def read_users(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le = 100)] = 100, 
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all() 

    return users


@app.post('/register')
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@app.on_event("startup")
def on_startup(): 
    create_db_and_tables()