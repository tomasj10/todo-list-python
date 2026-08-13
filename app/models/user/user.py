from sqlmodel import Field

from app.models.user.user_base import UserBase

class User(UserBase, table=True): 
    __tablename__ = "users"

    name: str | None = Field(index = True)
    password: str = Field(default=None)

    def to_json(self): 
        return {
            "name": self.name, 
            "email": self.email,
            "password": self.password
        }
    