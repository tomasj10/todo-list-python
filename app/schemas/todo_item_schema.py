from app.models.todo.todo_item_base import TodoItemBase

class TodoItemPublic(TodoItemBase): 
    id : int

class TodoItemCreate(TodoItemBase):
    pass

class TodoItemUpdate(TodoItemBase): 
    title: str | None = None
    description: str | None = None