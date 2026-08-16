from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.repository.todo_item_repository import TodoItemRepository
from app.schemas.todo_item_schema import TodoItemCreate


class TodoItemService:
    def __init__(self, session: Session) : 
        self.__to_do_item_repository = TodoItemRepository(session=session)

    def get_to_do_item_by_id(self, to_do_item_id: int) : 
        to_do_item = self.__to_do_item_repository.get_to_do_item_by_id(to_do_item_id=to_do_item_id)

        if to_do_item: 
            return to_do_item

        raise HTTPException(status_code=404, detail="To Do Item Not Found.")

    def create_to_do_item(self, to_do_item_details: TodoItemCreate) : 
        if self.__to_do_item_repository.to_do_item_exists_by_title(to_do_item_title=to_do_item_details.title): 
            raise HTTPException(status_code=409, detail="To Do Item already exists.")

        return self.__to_do_item_repository.create_to_do_item(todo_item_data=to_do_item_details)

    def get_all_to_do_items(self, page: int, limit: int): 
        return self.__to_do_item_repository.list_all_to_do_items(page=page, limit=limit)