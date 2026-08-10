from app.models.user.user_base import UserBase

class UserUpdate(UserBase):
    name: str | None = None
    email: str | None = None
    password: str | None = None