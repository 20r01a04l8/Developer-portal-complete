from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(self.model).filter(self.model.email == email).first()

    def get_active_user_by_email(self, email: str) -> Optional[User]:
        return (
            self.db.query(self.model)
            .filter(self.model.email == email, self.model.is_active == True)
            .first()
        )

    def email_exists(self, email: str) -> bool:
        return self.db.query(self.model).filter(self.model.email == email).first() is not None
