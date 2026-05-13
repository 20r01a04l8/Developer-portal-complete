from fastapi import APIRouter, Request
from app.core.proxy import ServiceClient

router = APIRouter()


@router.api_route("/projects/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def project_proxy(request: Request):
    return await ServiceClient.proxy_to_project_service(request)


@router.api_route("/projects", methods=["GET", "POST"])
async def project_list_proxy(request: Request):
    return await ServiceClient.proxy_to_project_service(request)


@router.api_route("/tasks/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def task_proxy(request: Request):
    return await ServiceClient.proxy_to_task_service(request)


@router.api_route("/tasks", methods=["GET", "POST"])
async def task_list_proxy(request: Request):
    return await ServiceClient.proxy_to_task_service(request)
