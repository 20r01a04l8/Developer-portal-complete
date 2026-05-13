from typing import Optional, List
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.project import Project
from app.core.exceptions import NotFoundException, ConflictException


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def create_project(self, project_data: ProjectCreate) -> Project:
        existing = self.repository.get_by_name(project_data.name)
        if existing:
            raise ConflictException(f"Project with name '{project_data.name}' already exists")
        
        return self.repository.create(project_data.model_dump())

    def get_project(self, project_id: int) -> Project:
        project = self.repository.get(project_id)
        if not project:
            raise NotFoundException(f"Project with id {project_id} not found")
        return project

    def get_all_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_projects_by_owner(self, owner: str, skip: int = 0, limit: int = 100) -> List[Project]:
        return self.repository.get_by_owner(owner, skip=skip, limit=limit)

    def get_projects_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Project]:
        return self.repository.get_by_status(status, skip=skip, limit=limit)

    def search_projects(self, query: str, skip: int = 0, limit: int = 100) -> List[Project]:
        return self.repository.search(query, skip=skip, limit=limit)

    def update_project(self, project_id: int, project_data: ProjectUpdate) -> Project:
        project = self.get_project(project_id)
        
        update_data = project_data.model_dump(exclude_unset=True)
        
        if "name" in update_data:
            existing = self.repository.get_by_name(update_data["name"])
            if existing and existing.id != project_id:
                raise ConflictException(f"Project with name '{update_data['name']}' already exists")
        
        updated = self.repository.update(project_id, update_data)
        if not updated:
            raise NotFoundException(f"Project with id {project_id} not found")
        
        return updated

    def delete_project(self, project_id: int) -> bool:
        project = self.get_project(project_id)
        return self.repository.delete(project_id)

    def count_projects(self) -> int:
        return self.repository.count()
