import httpx
from fastapi import Request, Response
from typing import Optional
from app.core.config import settings


class ServiceClient:
    @staticmethod
    async def forward_request(
        service_url: str,
        path: str,
        method: str,
        headers: dict,
        body: Optional[bytes] = None,
        params: Optional[dict] = None
    ) -> Response:
        async with httpx.AsyncClient() as client:
            url = f"{service_url}{path}"
            
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=body,
                params=params,
                timeout=30.0
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type")
            )

    @staticmethod
    async def proxy_to_auth_service(request: Request) -> Response:
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        
        path = request.url.path.replace("/api/v1/auth", "/api/v1")
        
        return await ServiceClient.forward_request(
            service_url=settings.auth_service_url,
            path=path,
            method=request.method,
            headers=headers,
            body=body,
            params=dict(request.query_params)
        )

    @staticmethod
    async def proxy_to_project_service(request: Request) -> Response:
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        
        path = request.url.path.replace("/api/v1/projects", "/api/v1/projects")
        
        return await ServiceClient.forward_request(
            service_url=settings.project_service_url,
            path=path,
            method=request.method,
            headers=headers,
            body=body,
            params=dict(request.query_params)
        )

    @staticmethod
    async def proxy_to_task_service(request: Request) -> Response:
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        
        path = request.url.path.replace("/api/v1/tasks", "/api/v1/tasks")
        
        return await ServiceClient.forward_request(
            service_url=settings.task_service_url,
            path=path,
            method=request.method,
            headers=headers,
            body=body,
            params=dict(request.query_params)
        )
