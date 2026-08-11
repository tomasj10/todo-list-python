from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.repository.user_repository import UserRepository
from app.schemas.create.user_create import UserCreate
from app.schemas.public.user_public import UserPublic
from app.schemas.login.user_in_login import UserInLogin
from app.schemas.token.user_with_token import UserWithToken
from app.core.security.hash_helper import HashHelper
from app.core.security.auth_handler import AuthHandler

class UserService: 
    def __init__(self, session: Session): 
        self.__user_repository = UserRepository(session=session)

    def signup(self, user_details: UserCreate) -> UserPublic :
        if self.__user_repository.user_exists_by_email(user_email=user_details.email): 
            raise HTTPException(status_code=400, detail="Please, Login")

        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password

        return self.__user_repository.create_user(user_data=user_details)


    def login(self, login_details : UserInLogin) -> UserWithToken : 
        if not self.__user_repository.user_exists_by_email(user_email=login_details.email): 
            raise HTTPException(status_code=404, detail="Please, create an account.")

        user = self.__user_repository.get_user_by_email(user_email=login_details.email)
        if HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.password): 
            token = AuthHandler.sign_jwt(user_email=login_details.email)
            if token: 
                return UserWithToken(token=token)
            raise HTTPException(status_code=500, detail="Unable to process request")
        raise HTTPException(status_code=400, detail="Please, check your credentials again")