from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.task import TaskRepository
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.core.logging import logger

router = APIRouter()


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    repository = TaskRepository(db)
    return TaskService(repository)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    logger.info(f"Creating task: {task.title}")
    created_task = service.create_task(task)
    logger.info(f"Task created with id: {created_task.id}")
    return created_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    logger.info(f"Fetching task with id: {task_id}")
    return service.get_task(task_id)


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: int | None = Query(None, gt=0),
    status: str | None = Query(None),
    priority: str | None = Query(None),
    search: str | None = Query(None),
    service: TaskService = Depends(get_task_service)
):
    logger.info(f"Listing tasks with filters - project_id: {project_id}, status: {status}, priority: {priority}, search: {search}")
    
    if search:
        tasks = service.search_tasks(search, skip=skip, limit=limit)
    elif project_id or status or priority:
        tasks = service.get_tasks_with_filters(
            project_id=project_id,
            status=status,
            priority=priority,
            skip=skip,
            limit=limit
        )
    else:
        tasks = service.get_all_tasks(skip=skip, limit=limit)
    
    total = service.count_tasks()
    
    return TaskListResponse(
        items=tasks,
        total=total,
        page=skip // limit + 1,
        size=len(tasks)
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    logger.info(f"Updating task with id: {task_id}")
    updated_task = service.update_task(task_id, task)
    logger.info(f"Task updated: {task_id}")
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    logger.info(f"Deleting task with id: {task_id}")
    service.delete_task(task_id)
    logger.info(f"Task deleted: {task_id}")
