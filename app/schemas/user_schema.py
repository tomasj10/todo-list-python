from pydantic import BaseModel

from app.models.user.user_base import UserBase

class UserPublic(UserBase):
    name : str

class UserCreate(UserBase): 
    name: str
    password : str

class UserUpdate(UserBase):
    name: str | None = None
    email: str | None = None
    password: str | None = None

class UserInLogin(UserBase): 
    password: str

class UserWithToken(BaseModel): 
    token: str