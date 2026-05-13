from typing import List
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task
from app.core.exceptions import NotFoundException


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task_data: TaskCreate) -> Task:
        return self.repository.create(task_data.model_dump())

    def get_task(self, task_id: int) -> Task:
        task = self.repository.get(task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found")
        return task

    def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_tasks_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.repository.get_by_project(project_id, skip=skip, limit=limit)

    def get_tasks_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.repository.get_by_status(status, skip=skip, limit=limit)

    def get_tasks_by_priority(self, priority: str, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.repository.get_by_priority(priority, skip=skip, limit=limit)

    def get_tasks_with_filters(
        self,
        project_id: int | None = None,
        status: str | None = None,
        priority: str | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        return self.repository.get_with_filters(
            project_id=project_id,
            status=status,
            priority=priority,
            skip=skip,
            limit=limit
        )

    def search_tasks(self, query: str, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.repository.search(query, skip=skip, limit=limit)

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        task = self.get_task(task_id)
        
        update_data = task_data.model_dump(exclude_unset=True)
        
        updated = self.repository.update(task_id, update_data)
        if not updated:
            raise NotFoundException(f"Task with id {task_id} not found")
        
        return updated

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        return self.repository.delete(task_id)

    def count_tasks(self) -> int:
        return self.repository.count()

    def count_tasks_by_project(self, project_id: int) -> int:
        return self.repository.count_by_project(project_id)

    def count_tasks_by_status(self, status: str) -> int:
        return self.repository.count_by_status(status)
