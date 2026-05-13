# Complete Backend Testing Guide - Step by Step

## 🎯 Overview

This guide will walk you through testing the complete microservices architecture:
- **Auth Service** (Port 8003) - Authentication
- **Project Service** (Port 8001) - Project management  
- **Task Service** (Port 8002) - Task management
- **API Gateway** (Port 8080) - Single entry point

---

## 📋 Prerequisites

### 1. Database Setup

Create three PostgreSQL databases:

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create databases
CREATE DATABASE auth_db;
CREATE DATABASE project_db;
CREATE DATABASE task_db;

-- Verify
\l

-- Exit
\q
```

### 2. Environment Configuration

**Auth Service** (`backend/auth-service/.env`):
```
APP_NAME=auth-service
DATABASE_URL=postgresql://postgres:password@localhost:5432/auth_db
JWT_SECRET_KEY=your-super-secret-key-min-32-chars-long-change-this
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
```

**Project Service** (`backend/project-service/.env`):
```
APP_NAME=project-service
DATABASE_URL=postgresql://postgres:password@localhost:5432/project_db
JWT_SECRET_KEY=your-super-secret-key-min-32-chars-long-change-this
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
```

**Task Service** (`backend/task-service/.env`):
```
APP_NAME=task-service
DATABASE_URL=postgresql://postgres:password@localhost:5432/task_db
JWT_SECRET_KEY=your-super-secret-key-min-32-chars-long-change-this
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
```

**API Gateway** (`backend/api-gateway/.env`):
```
APP_NAME=api-gateway
AUTH_SERVICE_URL=http://localhost:8003
PROJECT_SERVICE_URL=http://localhost:8001
TASK_SERVICE_URL=http://localhost:8002
JWT_SECRET_KEY=your-super-secret-key-min-32-chars-long-change-this
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 🚀 Step 1: Start Auth Service

```bash
cd backend/auth-service

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start service
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

**Verify Auth Service:**
```bash
curl http://localhost:8003/api/v1/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "auth-service"
}
```

---

## 🚀 Step 2: Start Project Service

Open a **new terminal**:

```bash
cd backend/project-service

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start service
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Verify Project Service:**
```bash
curl http://localhost:8001/api/v1/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "project-service",
  "version": "1.0.0",
  "database": "healthy"
}
```

---

## 🚀 Step 3: Start Task Service

Open a **new terminal**:

```bash
cd backend/task-service

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start service
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

**Verify Task Service:**
```bash
curl http://localhost:8002/api/v1/health
```

---

## 🚀 Step 4: Start API Gateway

Open a **new terminal**:

```bash
cd backend/api-gateway

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Start gateway
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Verify API Gateway:**
```bash
curl http://localhost:8080/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "version": "1.0.0"
}
```

---

## 🧪 Step 5: Test Authentication Flow

### 5.1 Register a New User

```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Test123456\",\"full_name\":\"Test User\"}"
```

**Expected Response (201 Created):**
```json
{
  "email": "test@example.com",
  "full_name": "Test User",
  "role": "user",
  "id": 1,
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "last_login": null
}
```

### 5.2 Login

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Test123456\"}"
```

**Expected Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**⚠️ IMPORTANT: Save the `access_token` for next steps!**

### 5.3 Verify Token

```bash
curl -X POST http://localhost:8080/api/v1/auth/verify \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"YOUR_ACCESS_TOKEN_HERE\"}"
```

**Expected Response:**
```json
{
  "valid": true,
  "user_id": 1,
  "email": "test@example.com",
  "role": "user",
  "message": null
}
```

---

## 🧪 Step 6: Test Project Service (via Gateway)

### 6.1 Create Project

```bash
curl -X POST http://localhost:8080/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d "{\"name\":\"My First Project\",\"owner\":\"test@example.com\",\"status\":\"active\"}"
```

**Expected Response (201 Created):**
```json
{
  "name": "My First Project",
  "owner": "test@example.com",
  "status": "active",
  "id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 6.2 List Projects

```bash
curl http://localhost:8080/api/v1/projects \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "items": [
    {
      "name": "My First Project",
      "owner": "test@example.com",
      "status": "active",
      "id": 1,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 1
}
```

### 6.3 Get Single Project

```bash
curl http://localhost:8080/api/v1/projects/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6.4 Update Project

```bash
curl -X PUT http://localhost:8080/api/v1/projects/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d "{\"status\":\"inactive\"}"
```

### 6.5 Filter Projects

```bash
# By status
curl "http://localhost:8080/api/v1/projects?status=active" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# By owner
curl "http://localhost:8080/api/v1/projects?owner=test@example.com" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Search
curl "http://localhost:8080/api/v1/projects?search=First" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6.6 Delete Project

```bash
curl -X DELETE http://localhost:8080/api/v1/projects/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response: 204 No Content**

---

## 🧪 Step 7: Test Task Service (via Gateway)

### 7.1 Create Task

```bash
curl -X POST http://localhost:8080/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d "{\"project_id\":1,\"title\":\"Implement authentication\",\"status\":\"todo\",\"priority\":\"high\"}"
```

**Expected Response (201 Created):**
```json
{
  "project_id": 1,
  "title": "Implement authentication",
  "status": "todo",
  "priority": "high",
  "id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 7.2 List Tasks

```bash
curl http://localhost:8080/api/v1/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7.3 Filter Tasks

```bash
# By project
curl "http://localhost:8080/api/v1/tasks?project_id=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# By status
curl "http://localhost:8080/api/v1/tasks?status=todo" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# By priority
curl "http://localhost:8080/api/v1/tasks?priority=high" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Multiple filters
curl "http://localhost:8080/api/v1/tasks?project_id=1&status=todo&priority=high" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7.4 Update Task

```bash
curl -X PUT http://localhost:8080/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d "{\"status\":\"in_progress\",\"priority\":\"critical\"}"
```

### 7.5 Delete Task

```bash
curl -X DELETE http://localhost:8080/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🧪 Step 8: Test Error Scenarios

### 8.1 Test Without Token (Should Fail)

```bash
curl http://localhost:8080/api/v1/projects
```

**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Missing or invalid authorization header"
}
```

### 8.2 Test With Invalid Token

```bash
curl http://localhost:8080/api/v1/projects \
  -H "Authorization: Bearer invalid_token_here"
```

**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Invalid or expired token"
}
```

### 8.3 Test Duplicate Email Registration

```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Test123456\"}"
```

**Expected Response (409 Conflict):**
```json
{
  "error": "User with email 'test@example.com' already exists",
  "status_code": 409
}
```

### 8.4 Test Invalid Login

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"WrongPassword\"}"
```

**Expected Response (401 Unauthorized):**
```json
{
  "error": "Invalid email or password",
  "status_code": 401
}
```

### 8.5 Test Validation Errors

```bash
# Missing required field
curl -X POST http://localhost:8080/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d "{\"owner\":\"test@example.com\"}"
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "error": "Validation error",
  "details": [...]
}
```

---

## 🧪 Step 9: Test Token Refresh

### 9.1 Wait for Token Expiration (or use expired token)

### 9.2 Refresh Token

```bash
curl -X POST http://localhost:8080/api/v1/auth/refresh \
  -H "X-Refresh-Token: YOUR_REFRESH_TOKEN"
```

**Expected Response:**
```json
{
  "access_token": "new_access_token...",
  "refresh_token": "new_refresh_token...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## 📊 Step 10: Verify All Services

### Check All Health Endpoints

```bash
# Auth Service
curl http://localhost:8003/api/v1/health

# Project Service  
curl http://localhost:8001/api/v1/health

# Task Service
curl http://localhost:8002/api/v1/health

# API Gateway
curl http://localhost:8080/health
```

**All should return healthy status**

---

## ✅ Success Checklist

- [ ] All 4 services running
- [ ] All databases created and migrated
- [ ] User registration successful
- [ ] User login successful
- [ ] Token verification working
- [ ] Projects CRUD working via gateway
- [ ] Tasks CRUD working via gateway
- [ ] Filtering working (projects & tasks)
- [ ] Authentication required for protected routes
- [ ] Invalid token rejected
- [ ] Error handling working correctly
- [ ] Token refresh working

---

## 🐛 Troubleshooting

### Issue: "relation 'users' does not exist"

**Solution:**
```bash
cd backend/auth-service
alembic upgrade head
```

### Issue: "Connection refused" to service

**Solution:**
- Check if service is running
- Verify port number
- Check firewall settings

### Issue: "Invalid token"

**Solution:**
- Verify JWT_SECRET_KEY is same across all services
- Check token expiration
- Ensure token format is correct

### Issue: Gateway can't reach services

**Solution:**
- Verify service URLs in gateway .env
- Check if services are running on correct ports
- Test services directly (bypass gateway)

---

## 📝 Testing with Postman

1. Import collection with these endpoints
2. Set environment variable for `access_token`
3. Use `{{access_token}}` in Authorization header
4. Test all endpoints systematically

---

## 🎯 Next Steps

After successful testing:

1. **Add More Users** - Test with multiple users
2. **Load Testing** - Use tools like Apache Bench or Locust
3. **Integration Tests** - Write automated tests
4. **Monitoring** - Add Prometheus/Grafana
5. **Logging** - Centralize logs with ELK stack
6. **CI/CD** - Set up automated deployment
7. **Docker** - Containerize services
8. **Kubernetes** - Orchestrate containers

---

**🎉 Congratulations! Your microservices architecture is fully tested and working!**
