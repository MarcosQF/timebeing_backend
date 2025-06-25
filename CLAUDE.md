# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Local Development
```bash
# Start development server
poetry run task run

# Code quality
poetry run task lint       # Run ruff linting
poetry run task pre_format # Fix linting issues
poetry run task format     # Format code with ruff

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
```

### Docker Development
```bash
# Start all services (app + PostgreSQL)
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs app
docker-compose logs db
```

## Architecture Overview

This is a **FastAPI backend** for a task/project management and habit tracking application. The project uses async patterns with SQLAlchemy 2.0 and PostgreSQL.

### Technology Stack
- FastAPI with async/await patterns
- SQLAlchemy 2.0 async ORM
- PostgreSQL (via asyncpg + psycopg)
- Alembic for migrations
- Poetry for dependency management
- Ruff for linting/formatting

### Project Structure
```
timebeing_backend/
├── main.py                 # FastAPI app entry point
├── settings.py             # Pydantic settings (DATABASE_URL from .env)
├── database.py             # Async SQLAlchemy session management
├── models/                 # Domain entities
├── schemas/                # Pydantic DTOs for API serialization
├── cruds/                  # Data access layer (repository pattern)
└── routers/                # API controllers
```

### Core Models & Relationships

**Task Model** (`models/task.py`):
- Self-referencing for subtasks (parent_task_id)
- Belongs to Project (project_id) 
- Status: Aberta, Andamento, Concluída
- Priority: Baixa, Média, Alta
- Location support (text + lat/lon coordinates)
- Duration estimation in "blocks"

**Project Model** (`models/project.py`):
- One-to-many with Tasks (cascade delete)
- Status: Criado, Andamento, Concluído

**Habit Model** (`models/habit.py`):
- Independent entity for habit tracking
- Simple scoring system

All models use UUID primary keys, TimestampMixin for created_at/updated_at, and have ai_context fields.

### API Structure

Base URL: `/api/v1`

**Endpoints:**
- `/tasks` - CRUD + `/tasks/{id}/subtasks`
- `/projects` - CRUD + `/projects/{id}/tasks` 
- `/habits` - CRUD operations

All use async database sessions via FastAPI dependency injection. PATCH endpoints use `exclude_unset=True` for partial updates.

### Key Patterns

1. **Clean Architecture**: Models → Schemas → CRUDs → Routers
2. **Async Repository Pattern**: CRUD classes handle data access
3. **Dependency Injection**: Database sessions injected via FastAPI Depends
4. **Soft Updates**: Partial updates using Pydantic exclude_unset
5. **Modern SQLAlchemy**: 2.0 async patterns throughout

### Coding Conventions

**SQLAlchemy Models**:
- Use `@Base.mapped_as_dataclass` decorator for all models
- All models inherit from `TimestampMixin` for created_at/updated_at
- Use `Mapped[Type]` annotations with `mapped_column()` for all fields
- UUID primary keys with `default=uuid.uuid4, init=False`
- Relationships use `init=False` and proper `back_populates`
- Enums inherit from `str, Enum` for API serialization

**Pydantic Schemas**:
- Separate schemas for Create, Public, List, and SoftUpdate operations
- Use `Field(default=...)` for default values in Create schemas
- SoftUpdate schemas have all optional fields with `None` defaults
- Import enums from models for consistency

**CRUD Operations**:
- Static methods in CRUD classes for all database operations
- Use `T_Session` type annotation for session parameters
- Raise `HTTPException` with `HTTPStatus` constants for errors
- Use `exclude_unset=True` in soft update operations
- Always commit and refresh after modifications

**API Routers**:
- Use `HTTPStatus` constants for status codes
- Consistent response models for all endpoints
- Proper dependency injection of database sessions
- Clear error messages in exception responses

**Database Configuration**:
- Async engine with `expire_on_commit=False`
- Database URL configuration via Pydantic settings
- Alembic configured for async operations with proper model imports

### Configuration

Settings loaded from `.env` file via Pydantic. Currently requires only `DATABASE_URL` for PostgreSQL connection.

### Missing Components

No authentication system or testing suite currently implemented.

## Project Documentation

- API schema is located at `@ai_docs/api_schema.md`
- Database schema is located at `@ai_docs/database_diagram.md`