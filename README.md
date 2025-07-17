# Task Management System

## Overview
This Task Management System is a robust backend API built with FastAPI and PostgreSQL, designed to handle task creation, retrieval, updating, and deletion. The system supports task categorization, prioritization, and deadline management with comprehensive filtering and sorting capabilities.

## Key Features
- **CRUD Operations**: Create, read, update, and delete tasks
- **Task Attributes**: Title, description, category, priority (Low/Medium/High), deadline
- **Advanced Filtering**: Filter by category, priority, or deadline range
- **Sorting**: Sort by creation date, priority, or deadline
- **Validation**: Strict input validation for all fields
- **Comprehensive Error Handling**: Clear error messages for invalid requests
- **Automated Documentation**: Interactive API docs via Swagger UI
- **Unit Tests**: Extensive test coverage for all core functionality

## Design Decisions

### Database Schema
```plaintext
tasks
├── id (PK, Integer)
├── title (String, Not Null)
├── description (String, Optional)
├── category (String, Optional)
├── priority (Enum: Low/Medium/High, Default: Medium)
├── deadline (DateTime, Optional)
├── created_at (DateTime, Default: utcnow)
└── updated_at (DateTime, Default: utcnow, OnUpdate: utcnow)
```

**Rationale**:
- Used PostgreSQL for reliability and scalability
- Created separate datetime fields for tracking creation and updates
- Implemented priority as an enum for data integrity
- Added indexes on frequently filtered fields (category, priority, deadline)

### API Design
- RESTful principles with resource-based endpoints
- Semantic HTTP status codes (200, 201, 400, 404, 500)
- Consistent JSON input/output formats
- Comprehensive error responses with details
- Query parameters for filtering and sorting

### Validation
- Title: Required and non-empty
- Deadline: Must be in the future
- Priority: Must be one of Low, Medium, High
- Category: Maximum 50 characters
- Description: Maximum 500 characters

## API Documentation

### Interactive Documentation
Access automatically generated documentation:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

### Endpoints

#### 1. Create Task
**POST** `/tasks`
```json
{
  "title": "Complete project",
  "description": "Finish the API implementation",
  "category": "Work",
  "priority": "High",
  "deadline": "2025-12-31T23:59:59"
}
```

**Success Response** (201 Created):
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the API implementation",
  "category": "Work",
  "priority": "High",
  "deadline": "2025-12-31T23:59:59",
  "created_at": "2025-07-17T10:30:00",
  "updated_at": "2025-07-17T10:30:00"
}
```

#### 2. List Tasks
**GET** `/tasks`
- **Filters**:
  - `category`: Filter by category
  - `priority`: Filter by priority
  - `start_date`: Minimum deadline (inclusive)
  - `end_date`: Maximum deadline (inclusive)
- **Sorting**:
  - `sort_by`: One of `created_at` (default), `priority`, or `deadline`

**Example**:  
`GET /tasks?category=Work&priority=High&sort_by=deadline`

**Response**:
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the API implementation",
    "category": "Work",
    "priority": "High",
    "deadline": "2025-12-31T23:59:59",
    "created_at": "2025-07-17T10:30:00",
    "updated_at": "2025-07-17T10:30:00"
  },
  // ... other tasks
]
```

#### 3. Get Task
**GET** `/tasks/{id}`  
`GET /tasks/1`

**Response**:
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the API implementation",
  "category": "Work",
  "priority": "High",
  "deadline": "2025-12-31T23:59:59",
  "created_at": "2025-07-17T10:30:00",
  "updated_at": "2025-07-17T10:30:00"
}
```

#### 4. Update Task
**PUT** `/tasks/{id}`  
```json
{
  "title": "Updated task title",
  "priority": "Medium"
}
```

**Response**:
```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Finish the API implementation",
  "category": "Work",
  "priority": "Medium",
  "deadline": "2025-12-31T23:59:59",
  "created_at": "2025-07-17T10:30:00",
  "updated_at": "2025-07-17T10:35:22"
}
```

#### 5. Delete Task
**DELETE** `/tasks/{id}`  
`DELETE /tasks/1`

**Response**: 204 No Content

### Error Responses
```json
// 400 Bad Request (Validation Error)
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title cannot be empty",
      "type": "value_error"
    }
  ]
}

// 404 Not Found
{
  "detail": "Task not found"
}

// 500 Internal Server Error
{
  "detail": "Database error"
}
```

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task-management-system.git
   cd task-management-system
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
   - Create a new database
   - Update the connection string in `app/main.py`:
     ```python
     DATABASE_URL = "postgresql://<user>:<password>@<host>/<database>"
     ```

### Running the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at:  
http://localhost:8000

### Testing
Run the test suite with:
```bash
pytest test_main.py
```

Test coverage includes:
- Task creation with valid/invalid inputs
- Retrieval of single and multiple tasks
- Updating task details
- Task deletion
- Filtering and sorting functionality
- Error handling scenarios