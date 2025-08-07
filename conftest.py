# conftest.py

import pytest
import uuid
import requests

BASE_URL = "https://todo.pixegami.io"

@pytest.fixture
def new_task_payload():
    """
    Creates a fresh task payload with unique content and user ID.
    """
    return {
        "content": f"Test content {uuid.uuid4().hex}",
        "user_id": f"test_user_{uuid.uuid4().hex}",
        "is_done": False
    }

@pytest.fixture
def create_task(new_task_payload):
    """
    Creates a new task using the API and returns task_id and user_id.
    """
    response = requests.put(f"{BASE_URL}/create-task", json=new_task_payload)
    assert response.status_code == 200

    task = response.json()["task"]
    return {
        "task_id": task["task_id"],
        "user_id": new_task_payload["user_id"]
    }
