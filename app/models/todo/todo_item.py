from sqlmodel import Field

from .todo_item_base import TodoItemBase

class TodoItem(TodoItemBase, table=True):
    __tablename__ = "todo_item"

    id : int = Field(default = None, primary_key = True)
    
