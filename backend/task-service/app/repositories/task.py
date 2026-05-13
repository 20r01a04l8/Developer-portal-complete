from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        return (
            self.db.query(self.model)
            .filter(self.model.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Task]:
        return (
            self.db.query(self.model)
            .filter(self.model.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_priority(self, priority: str, skip: int = 0, limit: int = 100) -> List[Task]:
        return (
            self.db.query(self.model)
            .filter(self.model.priority == priority)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_project_and_status(
        self, project_id: int, status: str, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            self.db.query(self.model)
            .filter(
                and_(
                    self.model.project_id == project_id,
                    self.model.status == status
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_project_and_priority(
        self, project_id: int, priority: str, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            self.db.query(self.model)
            .filter(
                and_(
                    self.model.project_id == project_id,
                    self.model.priority == priority
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_filters(
        self,
        project_id: int | None = None,
        status: str | None = None,
        priority: str | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        query = self.db.query(self.model)
        
        filters = []
        if project_id is not None:
            filters.append(self.model.project_id == project_id)
        if status is not None:
            filters.append(self.model.status == status)
        if priority is not None:
            filters.append(self.model.priority == priority)
        
        if filters:
            query = query.filter(and_(*filters))
        
        return query.offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(func.count(self.model.id)).scalar()

    def count_by_project(self, project_id: int) -> int:
        return (
            self.db.query(func.count(self.model.id))
            .filter(self.model.project_id == project_id)
            .scalar()
        )

    def count_by_status(self, status: str) -> int:
        return (
            self.db.query(func.count(self.model.id))
            .filter(self.model.status == status)
            .scalar()
        )

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Task]:
        search_pattern = f"%{query}%"
        return (
            self.db.query(self.model)
            .filter(self.model.title.ilike(search_pattern))
            .offset(skip)
            .limit(limit)
            .all()
        )
