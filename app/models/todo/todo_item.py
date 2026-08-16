from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional

from .todo_item_base import TodoItemBase

if TYPE_CHECKING:
    from app.models.user.user import User

class TodoItem(TodoItemBase, table=True):
    __tablename__ = "todo_item"

    id : int = Field(default = None, primary_key = True)
    user_id : str | None =  Field(default=None, foreign_key="users.email")
    user: Optional["User"] = Relationship(back_populates="todo_items")