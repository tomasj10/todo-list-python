from typing import List, Optional

from app.models.todo.todo_item import TodoItem
from app.schemas.todo_item_schema import TodoItemCreate, TodoItemPublic, TodoItemUpdate
from .base_repository import BaseRepository


class TodoItemRepository(BaseRepository): 
    def create_to_do_item(self, todo_item_data: TodoItemCreate, user_email: str) : 
        new_to_do_item = TodoItem(**todo_item_data.model_dump(), user_id=user_email)

        self.session.add(instance=new_to_do_item)
        self.session.commit()
        self.session.refresh(new_to_do_item)

        return new_to_do_item

    def update_to_do_item(self, todo_item_id: int, todo_item_data: TodoItemUpdate) : 
        updated_to_do_item = self.session.query(TodoItem).get(todo_item_id)

        if not updated_to_do_item: 
            return None

        updated_dict = todo_item_data.model_dump(exclude_unset= True)

        for key, value in updated_dict.items(): 
            setattr(updated_to_do_item, key, value)

        self.session.add(updated_to_do_item)
        self.session.commit()
        self.session.refresh(updated_to_do_item)

        return updated_to_do_item

    def delete_to_do_item(self, to_do_item_id: int) -> bool : 
       item = self.session.get(TodoItem, to_do_item_id)
       if not item: 
           return False

       self.session.delete(item)
       self.session.commit()

       return True
       

    def to_do_item_exists_by_id(self, to_do_item_id: int) -> bool : 
        return bool(self.session.query(TodoItem).get(to_do_item_id))

    def to_do_item_exists_by_title(self, to_do_item_title: str) -> bool : 
        return bool(self.session.query(TodoItem).filter(TodoItem.title == to_do_item_title).first())

    def get_to_do_item_by_id(self, to_do_item_id: int) -> Optional[TodoItemPublic] : 
        return self.session.query(TodoItem).filter(TodoItem.id == to_do_item_id).first()

    def list_all_to_do_items(self, page: int, limit: int) -> List[TodoItem] :  
        return self.session.query(TodoItem).offset(offset=page).limit(limit=limit).all()

    def to_do_item_belongs_user(self, to_do_item_id: int, user_id: str) :
        return self.session.query(TodoItem).filter(TodoItem.user_id == user_id).filter(TodoItem.id == to_do_item_id).first() != None 