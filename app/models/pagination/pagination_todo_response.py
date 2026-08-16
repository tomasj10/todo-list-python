from pydantic import BaseModel

from app.schemas.todo_item_schema import TodoItemPublic

class PaginationTodoResponse(BaseModel): 
    data: list[TodoItemPublic]
    page: int
    limit: int
    total: int
