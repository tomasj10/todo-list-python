from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.repository.user_repository import UserRepository
from app.schemas.create.user_create import UserCreate
from app.schemas.public.user_public import UserPublic

class UserService: 
    def __init__(self, session: Session): 
        self.__user_repository = UserRepository(session=session)

    def signup(self, user_details: UserCreate) -> UserPublic :
        if self.__user_repository.user_exists_by_email(user_email=user_details.email): 
            raise HTTPException(status_code=400, detail="Please, Login")

        hashed_password = "1"
        user_details.password = hashed_password
        return self.__user_repository.create_user(user_data=user_details)

    def login(self, login_details : UserInLogin) -> UserWithToken : 
