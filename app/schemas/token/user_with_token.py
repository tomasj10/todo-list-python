from pydantic import BaseModel

from app.models.user.user_base import UserBase

class UserWithToken(BaseModel): 
    token: str
