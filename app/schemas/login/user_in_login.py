from app.models.user.user_base import UserBase

class UserInLogin(UserBase): 
    email: str
    password: str