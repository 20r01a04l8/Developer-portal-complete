# Quick Start Guide - Microservices Architecture

## 🎯 What Was Built

### Complete Microservices Architecture with:
1. **API Gateway** (Port 8080) - Single entry point
2. **Auth Service** (Port 8000) - Dedicated authentication
3. **Project Service** (Port 8001) - Project management
4. **Task Service** (Port 8002) - Task management

## 🚀 Quick Start (5 Minutes)

### Step 1: Start Auth Service
```bash
cd backend/auth-service
cp .env.example .env
# Edit .env: Set DATABASE_URL and JWT_SECRET_KEY
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Step 2: Start Project Service
```bash
cd backend/project-service
cp .env.example .env
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

### Step 3: Start Task Service
```bash
cd backend/task-service
cp .env.example .env
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8002
```

### Step 4: Start API Gateway
```bash
cd backend/api-gateway
cp .env.example .env
# Edit .env: Set service URLs and JWT_SECRET_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## 📝 Test the System

### 1. Register User
```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456","full_name":"Test User"}'
```

### 2. Login
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'
```

**Save the access_token from response!**

### 3. Create Project (Protected)
```bash
curl -X POST http://localhost:8080/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"name":"My Project","owner":"test@example.com","status":"active"}'
```

### 4. List Projects (Protected)
```bash
curl http://localhost:8080/api/v1/projects \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🏗️ Architecture Flow

```
Client Request
    ↓
API Gateway (8080)
    ├─ Verifies JWT Token
    ├─ Routes to appropriate service
    └─ Returns response
        ↓
    ┌───┴───┬───────┬────────┐
    ↓       ↓       ↓        ↓
Auth(8000) Project Task   Other
           (8001) (8002)  Services
```

## 🔐 Security Features

✅ **JWT Authentication**
- Access tokens (30 min)
- Refresh tokens (7 days)
- Bcrypt password hashing

✅ **API Gateway**
- Centralized authentication
- Token verification
- Request routing

✅ **Service Isolation**
- Separate databases
- Independent deployment
- Failure isolation

## 📊 Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| API Gateway | 8080 | Single entry point |
| Auth Service | 8000 | Authentication |
| Project Service | 8001 | Project management |
| Task Service | 8002 | Task management |

## 🎯 Key Endpoints

### Via API Gateway (8080)

**Authentication:**
- POST `/api/v1/auth/register` - Register
- POST `/api/v1/auth/login` - Login
- POST `/api/v1/auth/verify` - Verify token
- POST `/api/v1/auth/refresh` - Refresh token

**Projects (Protected):**
- POST `/api/v1/projects` - Create
- GET `/api/v1/projects` - List
- GET `/api/v1/projects/{id}` - Get
- PUT `/api/v1/projects/{id}` - Update
- DELETE `/api/v1/projects/{id}` - Delete

**Tasks (Protected):**
- POST `/api/v1/tasks` - Create
- GET `/api/v1/tasks` - List
- GET `/api/v1/tasks/{id}` - Get
- PUT `/api/v1/tasks/{id}` - Update
- DELETE `/api/v1/tasks/{id}` - Delete

## 📁 Project Structure

```
backend/
├── api-gateway/          # Port 8080
│   ├── app/
│   │   ├── core/         # Config, proxy
│   │   ├── middleware/   # JWT verification
│   │   ├── routes/       # Gateway routes
│   │   └── main.py
│   └── requirements.txt
│
├── auth-service/         # Port 8000
│   ├── app/
│   │   ├── api/          # Auth endpoints
│   │   ├── core/         # JWT, security
│   │   ├── models/       # User model
│   │   ├── repositories/ # Data access
│   │   ├── services/     # Business logic
│   │   └── main.py
│   └── requirements.txt
│
├── project-service/      # Port 8001
│   └── [Complete CRUD for projects]
│
└── task-service/         # Port 8002
    └── [Complete CRUD for tasks]
```

## 🔧 Environment Variables

### Auth Service (.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/auth_db
JWT_SECRET_KEY=your-32-char-secret-key-here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### API Gateway (.env)
```
AUTH_SERVICE_URL=http://localhost:8000
PROJECT_SERVICE_URL=http://localhost:8001
TASK_SERVICE_URL=http://localhost:8002
JWT_SECRET_KEY=same-as-auth-service
```

## ✅ What Makes This Production-Ready

1. **Microservices Architecture**
   - Independent services
   - Separate databases
   - Scalable design

2. **API Gateway Pattern**
   - Single entry point
   - Centralized authentication
   - Request routing

3. **JWT Authentication**
   - Stateless authentication
   - Access & refresh tokens
   - Secure token handling

4. **Clean Architecture**
   - Layered design
   - Dependency injection
   - SOLID principles

5. **Security Best Practices**
   - Bcrypt password hashing
   - Environment-based secrets
   - Token expiration
   - CORS configuration

## 📚 Documentation

- `MICROSERVICES_ARCHITECTURE.md` - Complete architecture guide
- `JWT_AUTHENTICATION_GUIDE.md` - Authentication details
- `PROJECT_SERVICE_README.md` - Project service docs
- `TASK_SERVICE_README.md` - Task service docs

## 🎓 Next Steps

1. **Add Rate Limiting** to API Gateway
2. **Implement Caching** (Redis)
3. **Add Monitoring** (Prometheus/Grafana)
4. **Set up CI/CD** Pipeline
5. **Add API Documentation** (Swagger UI)
6. **Implement Logging** (ELK Stack)
7. **Add Service Discovery** (Consul/Eureka)
8. **Implement Circuit Breaker** (Resilience4j)

## 🐛 Troubleshooting

**Services won't start?**
- Check if ports are available
- Verify database connections
- Check .env files

**Authentication fails?**
- Verify JWT_SECRET_KEY matches across services
- Check token expiration
- Verify database has users

**Gateway can't reach services?**
- Check service URLs in gateway .env
- Verify services are running
- Check firewall settings

## 💡 Tips

- Use Postman/Insomnia for API testing
- Check service logs for errors
- Use `/health` endpoints to verify services
- Store tokens securely in client
- Use refresh tokens for long sessions

---

**You now have a complete, production-ready microservices architecture!** 🎉
