# API Schema Documentation

This document provides comprehensive documentation for the TimeBeing Backend API endpoints, request/response schemas, and data models.

## Base Configuration

- **Base URL**: `/api/v1`
- **Content-Type**: `application/json`
- **Response Format**: JSON

## Authentication

Currently, no authentication is implemented.

## Tasks API

### Endpoints

#### `GET /api/v1/tasks`
List all tasks.

**Response**: `200 OK`
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "parent_task_id": "uuid | null",
      "project_id": "uuid | null", 
      "description": "string | null",
      "due_date": "datetime | null",
      "status": "Aberta | Andamento | Concluída",
      "priority": "Baixa | Média | Alta",
      "duration_estimate_blocks": "integer | null",
      "location_text": "string | null",
      "location_lat": "decimal | null",
      "location_lon": "decimal | null"
    }
  ]
}
```

#### `GET /api/v1/tasks/{task_id}`
Get a specific task by ID.

**Parameters**:
- `task_id` (path): UUID of the task

**Response**: `200 OK`
```json
{
  "id": "uuid",
  "title": "string",
  "parent_task_id": "uuid | null",
  "project_id": "uuid | null",
  "description": "string | null", 
  "due_date": "datetime | null",
  "status": "Aberta | Andamento | Concluída",
  "priority": "Baixa | Média | Alta",
  "duration_estimate_blocks": "integer | null",
  "location_text": "string | null",
  "location_lat": "decimal | null",
  "location_lon": "decimal | null"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Task not found"
}
```

#### `GET /api/v1/tasks/{task_id}/subtasks`
List all subtasks of a specific task.

**Parameters**:
- `task_id` (path): UUID of the parent task

**Response**: `200 OK`
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "parent_task_id": "uuid",
      "project_id": "uuid | null",
      "description": "string | null",
      "due_date": "datetime | null", 
      "status": "Aberta | Andamento | Concluída",
      "priority": "Baixa | Média | Alta",
      "duration_estimate_blocks": "integer | null",
      "location_text": "string | null",
      "location_lat": "decimal | null",
      "location_lon": "decimal | null"
    }
  ]
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Parent task not found"
}
```

#### `POST /api/v1/tasks`
Create a new task.

**Request Body**:
```json
{
  "title": "string",
  "description": "string | null",
  "due_date": "datetime | null",
  "status": "Aberta | Andamento | Concluída", // default: "Aberta"
  "priority": "Baixa | Média | Alta", // default: "Baixa"
  "duration_estimate_blocks": "integer | null",
  "location_text": "string | null",
  "location_lat": "decimal | null",
  "location_lon": "decimal | null",
  "ai_context_text": "string | null",
  "parent_task_id": "uuid | null",
  "project_id": "uuid | null"
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid",
  "title": "string",
  "parent_task_id": "uuid | null",
  "project_id": "uuid | null",
  "description": "string | null",
  "due_date": "datetime | null",
  "status": "Aberta | Andamento | Concluída",
  "priority": "Baixa | Média | Alta",
  "duration_estimate_blocks": "integer | null",
  "location_text": "string | null",
  "location_lat": "decimal | null",
  "location_lon": "decimal | null"
}
```

#### `PATCH /api/v1/tasks/{task_id}`
Partially update a task.

**Parameters**:
- `task_id` (path): UUID of the task

**Request Body** (all fields optional):
```json
{
  "title": "string",
  "parent_task_id": "uuid | null",
  "project_id": "uuid | null",
  "description": "string | null",
  "due_date": "datetime | null",
  "status": "Aberta | Andamento | Concluída",
  "priority": "Baixa | Média | Alta",
  "duration_estimate_blocks": "integer | null",
  "location_text": "string | null",
  "location_lat": "decimal | null",
  "location_lon": "decimal | null",
  "ai_context_text": "string | null"
}
```

**Response**: `200 OK`
```json
{
  "id": "uuid",
  "title": "string",
  "parent_task_id": "uuid | null",
  "project_id": "uuid | null",
  "description": "string | null",
  "due_date": "datetime | null",
  "status": "Aberta | Andamento | Concluída",
  "priority": "Baixa | Média | Alta",
  "duration_estimate_blocks": "integer | null",
  "location_text": "string | null",
  "location_lat": "decimal | null",
  "location_lon": "decimal | null"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Task not found"
}
```

#### `DELETE /api/v1/tasks/{task_id}`
Delete a task.

**Parameters**:
- `task_id` (path): UUID of the task

**Response**: `200 OK`
```json
{
  "message": "Task has been deleted successfully"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Task not found"
}
```

## Projects API

### Endpoints

#### `GET /api/v1/projects`
List all projects.

**Response**: `200 OK`
```json
{
  "projects": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string | null",
      "status": "Criado | Andamento | Concluído"
    }
  ]
}
```

#### `GET /api/v1/projects/{project_id}`
Get a specific project by ID.

**Parameters**:
- `project_id` (path): UUID of the project

**Response**: `200 OK`
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "status": "Criado | Andamento | Concluído"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Project not found"
}
```

#### `GET /api/v1/projects/{project_id}/tasks`
List all tasks belonging to a specific project.

**Parameters**:
- `project_id` (path): UUID of the project

**Response**: `200 OK`
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "parent_task_id": "uuid | null",
      "project_id": "uuid",
      "description": "string | null",
      "due_date": "datetime | null",
      "status": "Aberta | Andamento | Concluída",
      "priority": "Baixa | Média | Alta",
      "duration_estimate_blocks": "integer | null",
      "location_text": "string | null",
      "location_lat": "decimal | null",
      "location_lon": "decimal | null"
    }
  ]
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Project not found"
}
```

#### `POST /api/v1/projects`
Create a new project.

**Request Body**:
```json
{
  "title": "string",
  "description": "string | null",
  "status": "Criado | Andamento | Concluído", // default: "Criado"
  "ai_context_text": "string | null"
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "status": "Criado | Andamento | Concluído"
}
```

#### `PATCH /api/v1/projects/{project_id}`
Partially update a project.

**Parameters**:
- `project_id` (path): UUID of the project

**Request Body** (all fields optional):
```json
{
  "title": "string",
  "description": "string | null",
  "status": "Criado | Andamento | Concluído"
}
```

**Response**: `200 OK`
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "status": "Criado | Andamento | Concluído"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Project not found"
}
```

#### `DELETE /api/v1/projects/{project_id}`
Delete a project and all its associated tasks.

**Parameters**:
- `project_id` (path): UUID of the project

**Response**: `200 OK`
```json
{
  "message": "Project has been deleted succesfully"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Project not found"
}
```

## Habits API

### Endpoints

#### `GET /api/v1/habits`
List all habits.

**Response**: `200 OK`
```json
{
  "habits": [
    {
      "id": "uuid",
      "title": "string", 
      "description": "string | null",
      "current_score": "integer | null"
    }
  ]
}
```

#### `GET /api/v1/habits/{habit_id}`
Get a specific habit by ID.

**Parameters**:
- `habit_id` (path): UUID of the habit

**Response**: `200 OK`
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "current_score": "integer | null"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Habit not found"
}
```

#### `POST /api/v1/habits`
Create a new habit.

**Request Body**:
```json
{
  "title": "string",
  "description": "string | null",
  "current_score": "integer | null" // minimum: 0
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "current_score": "integer | null"
}
```

#### `PATCH /api/v1/habits/{habit_id}`
Partially update a habit.

**Parameters**:
- `habit_id` (path): UUID of the habit

**Request Body** (all fields optional):
```json
{
  "title": "string",
  "description": "string | null",
  "current_score": "integer | null"
}
```

**Response**: `200 OK`
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "current_score": "integer | null"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Habit not found"
}
```

#### `DELETE /api/v1/habits/{habit_id}`
Delete a habit.

**Parameters**:
- `habit_id` (path): UUID of the habit

**Response**: `200 OK`
```json
{
  "message": "Habit has been deleted successfully"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Habit not found"
}
```

## Data Models

### Task Model
- **id**: UUID (auto-generated, primary key)
- **title**: string (required)
- **description**: string (optional)
- **due_date**: datetime (optional)
- **status**: enum ["Aberta", "Andamento", "Concluída"] (default: "Aberta")
- **priority**: enum ["Baixa", "Média", "Alta"] (default: "Baixa")
- **duration_estimate_blocks**: integer (optional)
- **location_text**: string (optional)
- **location_lat**: decimal (optional, precision 10,7)
- **location_lon**: decimal (optional, precision 10,7)
- **ai_context_text**: string (optional)
- **parent_task_id**: UUID (optional, self-referencing foreign key)
- **project_id**: UUID (optional, foreign key to projects)
- **created_at**: datetime (auto-generated)
- **updated_at**: datetime (auto-updated)

### Project Model
- **id**: UUID (auto-generated, primary key)
- **title**: string (required)
- **description**: string (optional)
- **status**: enum ["Criado", "Andamento", "Concluído"] (default: "Criado")
- **ai_context_text**: string (optional)
- **created_at**: datetime (auto-generated)
- **updated_at**: datetime (auto-updated)

### Habit Model
- **id**: UUID (auto-generated, primary key)
- **title**: string (required)
- **description**: string (optional)
- **current_score**: integer (optional, minimum: 0)
- **ai_context_prompt**: string (optional)
- **created_at**: datetime (auto-generated)
- **updated_at**: datetime (auto-updated)

## Relationships

- **Projects** have a one-to-many relationship with **Tasks** (cascade delete)
- **Tasks** can have a self-referencing relationship for subtasks via `parent_task_id`
- **Habits** are independent entities with no relationships

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK` - Successful operation
- `201 Created` - Resource created successfully
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors

Error responses follow this format:
```json
{
  "detail": "Error message description"
}
```

## Notes

- All UUID fields are automatically generated
- Timestamps (created_at, updated_at) are automatically managed
- PATCH operations use partial updates (exclude_unset=True)
- Project deletion cascades to delete all associated tasks
- Location coordinates use decimal precision for accuracy
- Current implementation has no authentication or authorization