from fastapi import FastAPI, Query, HTTPException
from sqlmodel import select 
from typing import Annotated

from db_engine import create_db_and_tables, SessionDep
from user import User
from user_public import UserPublic
from user_create import UserCreate
from user_update import UserUpdate


app = FastAPI()


@app.post('/register', response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep) -> User:
    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return user

@app.get('/users', response_model=list[UserPublic])
def read_users(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le = 100)] = 100, 
):
    users = session.exec(select(User).offset(offset).limit(limit)).all() 

    return users

# Reading a single user
@app.get('/users/{email}', response_model=UserPublic)
def read_user(
    user_email: str,
    session: SessionDep, 
): 
    user = session.get(User, user_email)
    if not user: 
        raise HTTPException(status_code = 404, detail="User Not Found")

    return user

#Updating an user
@app.patch('/users/{email}', response_model=UserPublic)
def update_user(
    user_email: str, 
    user: UserUpdate,
    session: SessionDep,
):
    user_db = session.get(User, user_email)
    if not user: 
        raise HTTPException(status_code = 404, detail="User Not Found")

    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db

# Deleting an user
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