import json
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.todo_item_schema import TodoItemPublic, TodoItemCreate
from app.models.pagination.pagination_todo_response import PaginationTodoResponse
from app.db.database import SessionDep
from app.services.to_do_item_service import TodoItemService
from app.utils.protect_route import get_current_user
from app.schemas.user_schema import UserPublic


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

@router.post('', status_code=201, response_model=TodoItemPublic) 
def create_to_do_item(
    to_do_item_details: TodoItemCreate,
    session: SessionDep,
    user: UserPublic = Depends(get_current_user),
) : 
    try:
        return TodoItemService(session=session).create_to_do_item(to_do_item_details=to_do_item_details)
    except Exception as error:
        print(error)
        raise error

@router.get('', status_code=200, response_model=PaginationTodoResponse)
def get_all_to_do_items(
    session: SessionDep,
    page: int,
    limit: int,
    user: UserPublic = Depends(get_current_user)
) : 
    data = TodoItemService(session=session).get_all_to_do_items(page=page, limit=limit)

    return {
        "data": data, 
        "page": page,
        "limit": limit,
        "total": len(data)
    }