from sqlmodel import Field, SQLModel, Session 
from db_engine import get_session, create_db_and_tables

from user_base import UserBase

class User(UserBase, table=True): 
    password: str = Field(default=None)

    def to_json(self): 
        return {
            "name": self.name, 
            "email": self.email,
            "password": self.password
        }
    