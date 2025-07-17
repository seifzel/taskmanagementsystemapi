# task management system api
task management api project
Key Components Explained
Database Design:

PostgreSQL relational database

Tasks table with fields: id, title, description, category, priority, deadline, created_at, updated_at

Priority enum (Low/Medium/High) for data integrity

API Endpoints:

POST /tasks: Create task with validation

GET /tasks: Retrieve tasks with filtering/sorting

GET /tasks/{id}: Get single task

PUT /tasks/{id}: Update task

DELETE /tasks/{id}: Delete task

Validation:

Title non-empty check

Deadline must be in future

Priority enum validation

Pydantic model validation

Filtering & Sorting:

Filter by: category, priority, deadline range

Sort by: created_at (default), priority, deadline

Query parameters: category, priority, start_date, end_date, sort_by

Error Handling:

400: Validation errors

404: Task not found

500: Database errors

Detailed error messages

Testing:

Test CRUD operations

Validation tests

Filtering/sorting tests

Error scenario tests

Isolated test database

Documentation:

Automatic Swagger UI at /docs

Redoc at /redoc

Interactive API exploration
