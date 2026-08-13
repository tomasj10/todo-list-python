from fastapi import FastAPI, Depends

from app.db.database import create_db_and_tables
from app.routers import users
from app.utils.protect_route import get_current_user
from app.schemas.user_schema import UserPublic


app = FastAPI()

app.include_router(users.router)

@app.get("/protected")
def read_protected(user : UserPublic = Depends(get_current_user)) : 
    return "HELLO WORLD"

@app.on_event("startup")
def on_startup(): 
    create_db_and_tables()