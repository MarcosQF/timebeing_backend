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
# Start all services (app + PostgreSQL + PgAdmin + OpenTelemetry)
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

# Access services:
# - API: http://localhost:8000
# - PgAdmin: http://localhost:5050 (admin@timebeing.com / admin)
# - OpenTelemetry (Grafana): http://localhost:3001
```

## Architecture Overview

This is a **FastAPI backend** for a task/project management and habit tracking application. The project uses async patterns with SQLAlchemy 2.0 and PostgreSQL.

### Technology Stack
- FastAPI with async/await patterns
- SQLAlchemy 2.0 async ORM
- PostgreSQL (via psycopg)
- Alembic for migrations
- Poetry for dependency management
- UV for package resolution
- Ruff for linting/formatting
- OpenTelemetry for observability

### Project Structure
```
timebeing_backend/
├── main.py                 # FastAPI app entry point with CORS & lifespan
├── settings.py             # Pydantic settings (DATABASE_URL from .env)
├── database.py             # Async SQLAlchemy session management
├── logger.py               # Logging configuration
├── models/                 # Domain entities
│   ├── commom_mixins.py    # Shared model mixins (TimestampMixin)
│   ├── task.py             # Task model with self-referencing subtasks
│   ├── project.py          # Project model with cascading tasks
│   └── habit.py            # Habit tracking model
├── schemas/                # Pydantic DTOs for API serialization
├── cruds/                  # Data access layer (repository pattern)
└── routers/                # API controllers
```

### Core Models & Relationships

**Task Model** (`models/task.py`):
- Self-referencing for subtasks (parent_task_id → pai/subtasks relationship)
- Belongs to Project (project_id, nullable)
- Status: Boolean (completed/not completed)
- Priority: Baixa, Média, Alta (TaskPriorityState enum)
- Location support (text + lat/lon coordinates with Decimal precision)
- Duration estimation in "blocks" (integer)
- Focus flag (is_focus) for marking priority tasks
- Scheduling fields: due_date, scheduled_start_time, scheduled_end_time
- AI context field for additional metadata

**Project Model** (`models/project.py`):
- One-to-many with Tasks (cascade delete, selectin loading)
- Status: Criado, Andamento, Concluído (ProjectStatus enum)
- Priority: Baixa, Média, Alta (ProjectPriorityState enum)
- AI context field for additional metadata

**Habit Model** (`models/habit.py`):
- Independent entity for habit tracking
- Simple scoring system (current_score integer)
- AI context prompt field for personalization

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
5. **Modern SQLAlchemy**: 2.0 async patterns with mapped_as_dataclass
6. **Observability**: OpenTelemetry integration for monitoring
7. **CORS Support**: Configured for frontend development (ports 3000, 8080)

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

Docker services include:
- **PostgreSQL 15**: Main database (port 5432)
- **PgAdmin**: Database administration (port 5050)
- **OpenTelemetry**: Observability stack with Grafana LGTM (ports 3001, 4317)

### Missing Components

No authentication system or testing suite currently implemented.

### Development Notes

- Uses Python 3.13+ requirement
- Package management: Poetry + UV for resolution
- Database migrations handled by Alembic with auto-migration support
- CORS configured for common frontend dev ports
- OpenTelemetry auto-instrumentation enabled for FastAPI, PostgreSQL, and logging

## Project Documentation

- API schema is located at `@ai_docs/api_schema.md`
- Database schema is located at `@ai_docs/database_diagram.md`