# Routes for users
from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from sqlmodel import select 

from app.db.database import create_db_and_tables, SessionDep
from app.models.user.user import User
from app.schemas.user_schema import UserPublic, UserCreate, UserInLogin, UserWithToken, UserUpdate
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post('/register', status_code=201, response_model=UserPublic)
def create_user(
    user: UserCreate, 
    session: SessionDep
):
    try: 
        return UserService(session=session).signup(user_details=user)
    except Exception as error: 
        print(error)
        raise(error)

@router.post('/login', status_code=200, response_model=UserWithToken)
def login(
    login_details: UserInLogin,
    session: SessionDep,
): 
    try: 
        return UserService(session=session).login(login_details=login_details)
    except Exception as error: 
        print(error)
        raise error

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