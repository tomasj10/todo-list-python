from .base_repository import BaseRepository
from app.models.user.user import User
from app.schemas.create.user_create import UserCreate

class UserRepository(BaseRepository): 
    def create_user(self, user_data: UserCreate):
        new_user = User(**user_data.model_dump())

        self.session.add(instance=new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return new_user

    # Check if an user exists by its primary key 
    def user_exists_by_email(self, user_email: str) -> bool :
        user = self.session.query(User).filter_by(email=user_email).first()
        return bool(user)

    # Get an user by its primary key
    def get_user_by_email(self, user_email) -> User :
        user = self.session.query(User).filter_by(email=user_email).first()
        return user

    


         
