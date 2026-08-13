# Validate Data from the clients to create a new user

from app.models.user.user_base import UserBase

class UserCreate(UserBase): 
    name: str
    password : str