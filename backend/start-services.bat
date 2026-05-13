@echo off
echo Starting Backend Services...
echo.

start "API Gateway" cmd /k "cd api-gateway && uvicorn app.main:app --reload --port 8080"
timeout /t 2 /nobreak >nul

start "Project Service" cmd /k "cd project-service && uvicorn app.main:app --reload --port 8001"
timeout /t 2 /nobreak >nul

start "Task Service" cmd /k "cd task-service && uvicorn app.main:app --reload --port 8002"

echo.
echo All services started!
echo API Gateway: http://localhost:8080
echo Project Service: http://localhost:8001
echo Task Service: http://localhost:8002
echo.
pause
