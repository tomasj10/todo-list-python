# Routes for users
from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from sqlmodel import select 

from app.db.database import create_db_and_tables, SessionDep
from app.models.user.user import User
from app.schemas.public.user_public import UserPublic
from app.schemas.create.user_create import UserCreate
from app.schemas.update.user_update import UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post('/register', response_model=UserPublic)
def create_user(
    user: UserCreate, 
    session: SessionDep
):
    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.get('', response_model=list[UserPublic])
def read_users(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le = 100)] = 100, 
):
    users = session.exec(select(User).offset(offset).limit(limit)).all() 

    return users

# Reading a single user
@router.get('/{user_email}', response_model=UserPublic)
def read_user(
    user_email: str,
    session: SessionDep, 
): 
    user = session.get(User, user_email)
    if not user: 
        raise HTTPException(status_code = 404, detail="User Not Found")

    return user

#Updating an user
@router.patch('/{user_email}', response_model=UserPublic)
def update_user(
    user_email: str, 
    user: UserUpdate,
    session: SessionDep,
):
    user_db = session.get(User, user_email)
    if not user_db: 
        raise HTTPException(status_code = 404, detail="User Not Found")

    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db

# Deleting an user
@router.delete('/{user_email}')
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