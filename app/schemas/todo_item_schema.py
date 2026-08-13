from app.models.todo.todo_item_base import TodoItemBase

class TodoItemPublic(TodoItemBase): 
    id : int

class TodoItemCreate(TodoItemBase):
    id: int 

class TodoItemUpdate(TodoItemBase): 
    title: str | None = None
    description: str | None = None