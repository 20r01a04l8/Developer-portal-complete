# Troubleshooting & Quick Fixes

## Error: "relation 'users' does not exist"

This means the database table hasn't been created yet.

### Fix:

```bash
cd backend/auth-service
alembic upgrade head
```

If this doesn't work, check:

1. **Database exists:**
```sql
psql -U postgres
\l
-- Should see auth_db in the list
```

2. **Database URL is correct in .env:**
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/auth_db
```

3. **Alembic can connect:**
```bash
alembic current
```

4. **Force recreate migration:**
```bash
# Delete existing migration
rm alembic/versions/*.py

# Create new migration
alembic revision --autogenerate -m "initial"

# Apply migration
alembic upgrade head
```

---

## Services Not Starting

### Check Ports:
```bash
# Windows
netstat -ano | findstr :8003
netstat -ano | findstr :8001
netstat -ano | findstr :8002
netstat -ano | findstr :8080
```

### Kill Process on Port:
```bash
# Windows
taskkill /PID <PID> /F
```

---

## Gateway Can't Reach Services

### Update Gateway .env:
```
AUTH_SERVICE_URL=http://localhost:8003
PROJECT_SERVICE_URL=http://localhost:8001
TASK_SERVICE_URL=http://localhost:8002
```

### Test Services Directly:
```bash
curl http://localhost:8003/api/v1/health
curl http://localhost:8001/api/v1/health
curl http://localhost:8002/api/v1/health
```

---

## JWT Token Issues

### Ensure Same Secret Across Services:

All `.env` files should have the SAME `JWT_SECRET_KEY`:

```
JWT_SECRET_KEY=your-super-secret-key-min-32-chars-long
```

---

## Database Connection Issues

### Check PostgreSQL is Running:
```bash
# Windows
sc query postgresql-x64-14
```

### Test Connection:
```bash
psql -U postgres -d auth_db
```

---

## Quick Reset

### Reset Auth Service:
```bash
cd backend/auth-service
psql -U postgres -c "DROP DATABASE IF EXISTS auth_db;"
psql -U postgres -c "CREATE DATABASE auth_db;"
alembic upgrade head
```

### Reset Project Service:
```bash
cd backend/project-service
psql -U postgres -c "DROP DATABASE IF EXISTS project_db;"
psql -U postgres -c "CREATE DATABASE project_db;"
alembic upgrade head
```

### Reset Task Service:
```bash
cd backend/task-service
psql -U postgres -c "DROP DATABASE IF EXISTS task_db;"
psql -U postgres -c "CREATE DATABASE task_db;"
alembic upgrade head
```

---

## Verify Everything Works

```bash
# 1. Start all services
# 2. Test health endpoints
curl http://localhost:8003/api/v1/health
curl http://localhost:8001/api/v1/health
curl http://localhost:8002/api/v1/health
curl http://localhost:8080/health

# 3. Register user
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'

# 4. Login
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'
```

If all these work, your system is ready!
