from sqlmodel import SQLModel, Field

class TodoItemBase(SQLModel): 
    title : str = Field(default=None, index = True)
    description : str = Field(default=None)
    