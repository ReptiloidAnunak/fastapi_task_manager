# Task Manager - Test Assignment

A FastAPI task management application with comprehensive pytest testing.

## 📋 Requirements

**CRUD operations** for task management (create, get, get_list, update, delete):
- **ID** (auto-generated uuid)
- **Title** (string, 5-200 characters)
- **Description** (text, 5-1000 characters)  
- **Status**: `created`, `processing`, `completed`
- **Timestamps**: `created_at`, `updated_at`

## 🛠 Tech Stack

- ✅ **FastAPI** (3 points) - Modern web framework
- ✅ **pytest** (2 points) - Comprehensive test coverage
- ✅ **Postgres** - Data base
- ✅ **PEP8 Compliance** - Clean code standards
- ✅ **Docker** - Full containerization

## 🚀 Quick Start

```bash
# Start with Docker
./run_app.sh

# Access
# Web: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 📚 API Endpoints

```
GET    /api/tasks        # List tasks
POST   /api/tasks        # Create task
GET    /api/tasks/{id}   # Get task
PUT    /api/tasks/{id}   # Update task
DELETE /api/tasks/{id}   # Delete task
```

## 🧪 Testing

- ✅ All CRUD operations tested
- ✅ Data validation scenarios
- ✅ Error handling cases
- ✅ 90%+ test coverage