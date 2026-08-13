from sqlmodel import SQLModel, Field

class UserBase(SQLModel): 
    email: str = Field(primary_key=True, index=True)
