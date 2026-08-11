from app.models.user.user_base import UserBase

class UserWithToken(UserBase): 
    token: str
