### Key Components Explained

1. **Database Design**:
   - PostgreSQL relational database
   - Tasks table with fields: id, title, description, category, priority, deadline, created_at, updated_at
   - Priority enum (Low/Medium/High) for data integrity

2. **API Endpoints**:
   - `POST /tasks`: Create task with validation
   - `GET /tasks`: Retrieve tasks with filtering/sorting
   - `GET /tasks/{id}`: Get single task
   - `PUT /tasks/{id}`: Update task
   - `DELETE /tasks/{id}`: Delete task

3. **Validation**:
   - Title non-empty check
   - Deadline must be in future
   - Priority enum validation
   - Pydantic model validation

4. **Filtering & Sorting**:
   - Filter by: category, priority, deadline range
   - Sort by: created_at (default), priority, deadline
   - Query parameters: `category`, `priority`, `start_date`, `end_date`, `sort_by`

5. **Error Handling**:
   - 400: Validation errors
   - 404: Task not found
   - 500: Database errors
   - Detailed error messages

6. **Testing**:
   - Test CRUD operations
   - Validation tests
   - Filtering/sorting tests
   - Error scenario tests
   - Isolated test database

7. **Documentation**:
   - Automatic Swagger UI at `/docs`
   - Redoc at `/redoc`
   - Interactive API exploration

### How to Run

1. Install requirements:
```bash
pip install fastapi sqlalchemy psycopg2-binary pytest uvicorn
```

2. Start PostgreSQL service

3. Run migrations:
```python
# Create database tables from model definitions
Base.metadata.create_all(bind=engine)
```

4. Start service:
```bash
uvicorn app.main:app --reload
```

5. Run tests:
```bash
pytest
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`. The solution implements all requirements with production-grade practices including input validation, comprehensive error handling, and thorough test coverage.
