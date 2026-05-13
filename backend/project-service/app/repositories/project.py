from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db: Session):
        super().__init__(Project, db)

    def get_by_name(self, name: str) -> Optional[Project]:
        return self.db.query(self.model).filter(self.model.name == name).first()

    def get_by_owner(self, owner: str, skip: int = 0, limit: int = 100) -> List[Project]:
        return (
            self.db.query(self.model)
            .filter(self.model.owner == owner)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Project]:
        return (
            self.db.query(self.model)
            .filter(self.model.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        return self.db.query(func.count(self.model.id)).scalar()

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Project]:
        search_pattern = f"%{query}%"
        return (
            self.db.query(self.model)
            .filter(
                (self.model.name.ilike(search_pattern)) |
                (self.model.owner.ilike(search_pattern))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
