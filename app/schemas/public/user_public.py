# Returned TO the clients of API

from app.models.user.user_base import UserBase

class UserPublic(UserBase):
    def __str__(self): 
        return f"{self.name} with {self.email}"
