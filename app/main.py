from fastapi import FastAPI, Depends

from app.db.database import create_db_and_tables
from app.routers import users, to_do_item_router
from app.utils.protect_route import get_current_user
from app.schemas.user_schema import UserPublic


app = FastAPI()

app.include_router(users.router)
app.include_router(to_do_item_router.router)

@app.on_event("startup")
def on_startup(): 
    create_db_and_tables()