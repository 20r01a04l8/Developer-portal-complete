# Quick Start Guide

## Prerequisites

1. **Python 3.8+** installed
2. **Node.js 18+** installed
3. **PostgreSQL** running with databases created

## Database Setup

Create databases in PostgreSQL:

```sql
CREATE DATABASE project_db;
CREATE DATABASE task_db;
```

## Backend Setup

### Option 1: Use Startup Script (Recommended)

```bash
cd backend
start-services.bat
```

This will open 3 terminal windows for each service.

### Option 2: Manual Start

**Terminal 1 - API Gateway:**
```bash
cd backend/api-gateway
uvicorn app.main:app --reload --port 8080
```

**Terminal 2 - Project Service:**
```bash
cd backend/project-service
uvicorn app.main:app --reload --port 8001
```

**Terminal 3 - Task Service:**
```bash
cd backend/task-service
uvicorn app.main:app --reload --port 8002
```

## Frontend Setup

**Terminal 4 - React Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Verify Services

### Backend Health Checks
- API Gateway: http://localhost:8080/health
- Project Service: http://localhost:8001/health
- Task Service: http://localhost:8002/health

### API Documentation
- API Gateway: http://localhost:8080/docs
- Project Service: http://localhost:8001/docs
- Task Service: http://localhost:8002/docs

### Frontend
- React App: http://localhost:5173

## Architecture Flow

```
Frontend (5173)
    ↓
API Gateway (8080)
    ↓
    ├── Project Service (8001) → project_db
    └── Task Service (8002) → task_db
```

## Common Issues

### 1. ERR_CONNECTION_REFUSED
**Problem**: Backend services not running
**Solution**: Start all backend services using start-services.bat

### 2. Database Connection Error
**Problem**: PostgreSQL not running or databases not created
**Solution**: 
- Start PostgreSQL service
- Create databases: `CREATE DATABASE project_db; CREATE DATABASE task_db;`

### 3. Port Already in Use
**Problem**: Port 8080, 8001, or 8002 already in use
**Solution**: Kill the process or change port in .env files

### 4. Module Not Found
**Problem**: Dependencies not installed
**Solution**: 
- Backend: `pip install -r requirements.txt`
- Frontend: `npm install`

## Environment Variables

### Backend Services (.env)
Each service needs a `.env` file:

**api-gateway/.env:**
```env
APP_NAME=API Gateway
APP_VERSION=1.0.0
API_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

PROJECT_SERVICE_URL=http://localhost:8001
TASK_SERVICE_URL=http://localhost:8002
```

**project-service/.env:**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/project_db
```

**task-service/.env:**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/task_db
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8080/api/v1
```

## Testing the Application

1. **Start all services** (backend + frontend)
2. **Open browser**: http://localhost:5173
3. **Navigate to Projects**: Click "View Projects"
4. **Create a project**: Click "Create Project"
5. **Navigate to Tasks**: Click "View Tasks"
6. **Create a task**: Click "Create Task"

## Stopping Services

- Press `Ctrl+C` in each terminal window
- Or close the terminal windows

## Development Workflow

1. Make code changes
2. Services auto-reload (--reload flag)
3. Frontend hot-reloads automatically
4. Test changes in browser

## Production Build

### Backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Frontend
```bash
npm run build
npm run preview
```
