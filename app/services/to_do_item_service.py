from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.repository.todo_item_repository import TodoItemRepository
from app.schemas.todo_item_schema import TodoItemCreate, TodoItemUpdate


class TodoItemService:
    def __init__(self, session: Session) : 
        self.__to_do_item_repository = TodoItemRepository(session=session)

    def get_to_do_item_by_id(self, to_do_item_id: int) : 
        to_do_item = self.__to_do_item_repository.get_to_do_item_by_id(to_do_item_id=to_do_item_id)

        if to_do_item: 
            return to_do_item

        raise HTTPException(status_code=404, detail="To Do Item Not Found.")

    def create_to_do_item(self, to_do_item_details: TodoItemCreate, user_email: str) : 
        if self.__to_do_item_repository.to_do_item_exists_by_title(to_do_item_title=to_do_item_details.title): 
            raise HTTPException(status_code=409, detail="To Do Item already exists.")

        return self.__to_do_item_repository.create_to_do_item(
            todo_item_data=to_do_item_details,
            user_email=user_email
        )

    def update_to_do_item(self, to_do_item_id: int, to_do_item_details: TodoItemUpdate) : 
        if not self.__to_do_item_repository.to_do_item_exists_by_id(to_do_item_id=to_do_item_id): 
            raise HTTPException(status_code=404, detail="To Do Item does not exist")

        return self.__to_do_item_repository.update_to_do_item(
            todo_item_id=to_do_item_id, 
            todo_item_data= to_do_item_details
        )

    def get_all_to_do_items(self, page: int, limit: int): 
        return self.__to_do_item_repository.list_all_to_do_items(page=page, limit=limit)

    def delete_to_do_item(self, to_do_item_id: int, user_id: str) -> bool : 
        if not self.__to_do_item_repository.to_do_item_exists_by_id(to_do_item_id=to_do_item_id): 
            raise HTTPException(status_code=404, detail="To Do Item does not exist")

        if not self.__to_do_item_repository.to_do_item_belongs_user(to_do_item_id=to_do_item_id, user_id=user_id):
            raise HTTPException(status_code=403, detail="Unathorized")
        
        return self.__to_do_item_repository.delete_to_do_item(to_do_item_id=to_do_item_id)

    def to_do_item_belongs_user(self, to_do_item_id: int, user_id: int):
        if not self.__to_do_item_repository.to_do_item_exists_by_id(to_do_item_id=to_do_item_id): 
            raise HTTPException(status_code=404, detail="To Do Item does not exist")
        
        if self.__to_do_item_repository.to_do_item_belongs_user(to_do_item_id=to_do_item_id, user_id=user_id) == None : 
            raise HTTPException(status_code=403, detail="Forbidden")

        return True
        