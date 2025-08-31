import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from fastapi.testclient import TestClient
from api.main import app
from database.database import SessionLocal
from database.models import Task

testclient = TestClient(app)
db = SessionLocal()


test_task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "Pending"
        }


test_task_id = None


def test_index_response():
    response = testclient.get("/")
    assert response.status_code == 200


def  test_create_task():
    response = testclient.post(
        "/create-task",
        data=test_task_data
    )
    assert response.status_code == 200


def test_get_task():
    global test_task_id
    task = db.query(Task).filter(Task.title == 'Test Task').first()
    test_task_id = task.id
    task_page_response = testclient.get(f"/get-task/{test_task_id}")
    assert task is not None
    assert task.title == test_task_data['title']
    assert task.description == test_task_data['description']
    assert task.status == test_task_data['status']
    assert task_page_response.status_code == 200


def test_error_get_task():
    fake_id = random.randint(1000000, 10000000)
    response = testclient.get(f"/get-task/{fake_id}")
    assert response.status_code == 200


def test_update_task():
    global test_task_id
    task = db.query(Task).filter(Task.id == test_task_id).first()
    task.title = "Updated Test Task"
    task.description = "This is an updated test task"
    task.status = "Completed"
    db.commit()
    assert task.title == "Updated Test Task"
    assert task.description == "This is an updated test task"
    assert task.status == "Completed"
    assert task is not None


def test_delete_task():
    global test_task_id
    testclient.get(f"/delete-task/{test_task_id}")
    task = db.query(Task).filter(Task.id == test_task_id).first()
    assert task is None
    

def test_delete_error_task():
    fake_id = random.randint(1000000, 10000000)
    response = testclient.get(f"/delete-task/{fake_id}")
    assert response.status_code == 200



def test_task_timestamps():
    response = testclient.post("/create-task", data=test_task_data)
    assert response.status_code == 200
    
    task = db.query(Task).filter(Task.title == test_task_data["title"]).first()
    assert task.created_at is not None
    assert task.updated_at is None
    
    update_data = {
        "title": "Updated Task",
        "description": "Updated description", 
        "status": "completed"
    }
    
    response = testclient.post(f"/update-task/{task.id}", data=update_data)
    assert response.status_code == 200
    
    db.refresh(task)
    assert task.updated_at is not None
    assert task.updated_at > task.created_at
    db.query(Task).delete()
    db.commit()
    db.close()


def test_short_input():
    test_task_data = {
        "title": "T",
        "description": "D",
        "status": "Pending"
    }

    response_create = testclient.post(
    "/create-task",
    data=test_task_data
    )

    global test_task_id
    response_update = testclient.post(f"/update-task/{test_task_id}", data=test_task_data)

    assert response_create.status_code == 400
    assert response_update.status_code == 400