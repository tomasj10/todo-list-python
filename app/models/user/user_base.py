from sqlmodel import SQLModel, Field

class UserBase(SQLModel): 
    name: str | None = Field(index = True)
    email: str = Field(primary_key=True, index=True)
