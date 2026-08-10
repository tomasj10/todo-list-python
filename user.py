from sqlmodel import Field, SQLModel, Session 
from db_engine import get_session, create_db_and_tables

class User(SQLModel, table=True): 
    name: str = Field(default=None)
    email: str = Field(primary_key=True, index=True)
    password: str = Field(default=None)

    def to_json(self): 
        return {
            "name": self.name, 
            "email": self.email,
            "password": self.password
        }
    