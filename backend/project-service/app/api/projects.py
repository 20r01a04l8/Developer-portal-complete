from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.repositories.project import ProjectRepository
from app.services.project import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse
from app.core.logging import logger

router = APIRouter()


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    repository = ProjectRepository(db)
    return ProjectService(repository)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    logger.info(f"Creating project: {project.name}")
    created_project = service.create_project(project)
    logger.info(f"Project created with id: {created_project.id}")
    return created_project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    logger.info(f"Fetching project with id: {project_id}")
    return service.get_project(project_id)


@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    owner: str | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),
    service: ProjectService = Depends(get_project_service)
):
    logger.info(f"Listing projects with filters - owner: {owner}, status: {status}, search: {search}")
    
    if search:
        projects = service.search_projects(search, skip=skip, limit=limit)
    elif owner:
        projects = service.get_projects_by_owner(owner, skip=skip, limit=limit)
    elif status:
        projects = service.get_projects_by_status(status, skip=skip, limit=limit)
    else:
        projects = service.get_all_projects(skip=skip, limit=limit)
    
    total = service.count_projects()
    
    return ProjectListResponse(
        items=projects,
        total=total,
        page=skip // limit + 1,
        size=len(projects)
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    logger.info(f"Updating project with id: {project_id}")
    updated_project = service.update_project(project_id, project)
    logger.info(f"Project updated: {project_id}")
    return updated_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    logger.info(f"Deleting project with id: {project_id}")
    service.delete_project(project_id)
    logger.info(f"Project deleted: {project_id}")
