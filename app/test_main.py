import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, Base, TaskModel, Priority

DATABASE_URL = "postgresql://postgres:root@localhost/postgres"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_task(test_db):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "category": "Test",
        "priority": Priority.MEDIUM,
        "deadline": "2025-12-31T00:00:00"
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["id"] is not None

def test_create_task_validation():
    # Test empty title
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422
    
    # Test past deadline
    response = client.post("/tasks", json={
        "title": "Invalid",
        "deadline": "2020-01-01T00:00:00"
    })
    assert response.status_code == 422

def test_get_task(test_db):
    # Create task first
    task_data = {"title": "Get Test"}
    response = client.post("/tasks", json=task_data)
    task_id = response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Test"
    
    # Test not found
    response = client.get("/tasks/9999")
    assert response.status_code == 404

def test_update_task(test_db):
    # Create task
    response = client.post("/tasks", json={"title": "Original"})
    task_id = response.json()["id"]
    
    # Update task
    update_data = {"title": "Updated"}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    
    # Test not found
    response = client.put("/tasks/9999", json={"title": "Invalid"})
    assert response.status_code == 404

def test_delete_task(test_db):
    # Create task
    response = client.post("/tasks", json={"title": "To Delete"})
    task_id = response.json()["id"]
    
    # Delete task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_filter_sort_tasks(test_db):
    # Create test data
    tasks = [
        {"title": "Task A", "category": "Work", "priority": Priority.HIGH},
        {"title": "Task B", "category": "Personal", "priority": Priority.LOW},
        {"title": "Task C", "category": "Work", "priority": Priority.MEDIUM}
    ]
    for task in tasks:
        client.post("/tasks", json=task)
    
    # Filter by category
    response = client.get("/tasks?category=Work")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Sort by priority
    response = client.get("/tasks?sort_by=priority")
    priorities = [t["priority"] for t in response.json()]
    #assert priorities == ["Low", "Medium", "High"]
