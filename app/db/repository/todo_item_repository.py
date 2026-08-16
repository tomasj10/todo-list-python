from typing import List, Optional

from app.models.todo.todo_item import TodoItem
from app.schemas.todo_item_schema import TodoItemCreate, TodoItemPublic, TodoItemUpdate
from .base_repository import BaseRepository


class TodoItemRepository(BaseRepository): 
    def create_to_do_item(self, todo_item_data: TodoItemCreate) : 
        new_to_do_item = TodoItem(**todo_item_data.model_dump())

        self.session.add(instance=new_to_do_item)
        self.session.commit()
        self.session.refresh(new_to_do_item)

        return new_to_do_item

    def update_to_do_item(self, todo_item_id: id, todo_item_data: TodoItemUpdate) : 
        updated_to_do_item = self.session.query(TodoItem).get(todo_item_id)

        if not updated_to_do_item: 
            return None

        updated_to_do_item = todo_item_data
        self.session.commit()

        return updated_to_do_item

    def to_do_item_exists_by_id(self, to_do_item_id: int) -> bool : 
        return bool(self.session.query(TodoItem).filter(TodoItem.id == to_do_item_id).first())

    def to_do_item_exists_by_title(self, to_do_item_title: str) -> bool : 
            return bool(self.session.query(TodoItem).filter(TodoItem.title == to_do_item_title).first())

    def get_to_do_item_by_id(self, to_do_item_id: int) -> Optional[TodoItemPublic] : 
        return self.session.query(TodoItem).filter(TodoItem.id == to_do_item_id).first()

    def list_all_to_do_items(self) -> List[TodoItem] :  
        return self.session.query(TodoItem).all()