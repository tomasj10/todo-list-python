from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

from app.models.user.user_base import UserBase

if TYPE_CHECKING:
    from app.models.todo.todo_item import TodoItem

class User(UserBase, table=True): 
    __tablename__ = "users"

    name: str | None = Field(index = True)
    password: str = Field(default=None)

    todo_items: list["TodoItem"] = Relationship(back_populates="user")

    def to_json(self): 
        return {
            "name": self.name, 
            "email": self.email,
            "password": self.password
        }
    