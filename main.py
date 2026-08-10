from fastapi import FastAPI, Query, HTTPException
from user import User

from sqlmodel import select 
from db_engine import create_db_and_tables, SessionDep
from typing import Annotated

app = FastAPI()


@app.post('/register')
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@app.get('/users')
def read_users(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le = 100)] = 100, 
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all() 

    return users

# Reading a single user
@app.get('/users/{email}')
def read_user(
    user_email: str,
    session: SessionDep, 
) -> User : 
    user = session.get(User, user_email)
    if not user: 
        raise HTTPException(status_code = 404, detail="User Not Found")

    return user

# Deleting a user
@app.delete('/users/{email}')
def delete_user(
    user_email: str, 
    session: SessionDep,
): 
    user = session.get(User, user_email)
    if not user: 
        raise HTTPException(status_code = 404, detail="User Not Found")

    session.delete(user)
    session.commit()

    return {
        "ok": True
    }


@app.on_event("startup")
def on_startup(): 
    create_db_and_tables()