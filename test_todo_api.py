import requests
import uuid

# Base URL for the API we're testing
ENDPOINT = "https://todo.pixegami.io/"

# -------------------- TESTS --------------------

def test_can_call_endpoint():
    # Make sure the API is up and running
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    # Try creating a new task and check if it saves correctly
    payload = new_task_payload()
    response = create_task(payload)
    assert response.status_code == 200

    task_id = response.json()["task"]["task_id"]

    # Now try to fetch the task we just created
    get_response = get_task(task_id)
    assert get_response.status_code == 200

    task_data = get_response.json()

    # Check if the saved task matches what we sent
    assert task_data["content"] == payload["content"]
    assert task_data["user_id"] == payload["user_id"]
    print(task_data)  # Optional: see what the task looks like


def test_can_update_task():
    # First, create a new task
    payload = new_task_payload()
    create_response = create_task(payload)
    assert create_response.status_code == 200

    task_id = create_response.json()["task"]["task_id"]

    # Now, let's update the content and mark it as done
    updated_payload = {
        "content": "updated content",
        "task_id": task_id,
        "user_id": payload["user_id"],
        "is_done": True
    }

    update_response = update_task(updated_payload)
    assert update_response.status_code == 200

    # Let's fetch the updated task and check if the changes were saved
    get_response = get_task(task_id)
    assert get_response.status_code == 200
    updated_data = get_response.json()

    assert updated_data["content"] == "updated content"
    assert updated_data["is_done"] == True


def test_can_list_tasks():
    # Create 3 tasks under the same user to test listing
    user_id = f"test_user_{uuid.uuid4().hex}"
    task_count = 3

    for i in range(task_count):
        payload = {
            "content": f"task {i}",
            "user_id": user_id,
            "is_done": False
        }
        response = create_task(payload)
        assert response.status_code == 200

    # Now list all tasks for this user
    list_response = list_tasks(user_id)
    assert list_response.status_code == 200

    tasks = list_response.json()["tasks"]
    assert len(tasks) >= task_count  # Should include at least the 3 we created
    print(tasks)  # Optional: view the returned list


def test_can_delete_task():
    # Create a task first
    payload = new_task_payload()
    response = create_task(payload)
    assert response.status_code == 200
    task_id = response.json()["task"]["task_id"]

    # Delete the task
    delete_response = requests.delete(ENDPOINT + f"/delete-task/{task_id}")
    assert delete_response.status_code == 200

    # Try to get the deleted task — it should no longer exist
    get_response = get_task(task_id)
    assert get_response.status_code in [400, 404]  # API might return 404 or 400

# -------------------- HELPER FUNCTIONS --------------------

def create_task(payload):
    # Sends a request to create a task using the given payload
    return requests.put(ENDPOINT + "/create-task", json=payload)

def get_task(task_id):
    # Fetches a task by its ID
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def update_task(payload):
    # Updates a task with new content or status
    return requests.put(ENDPOINT + "/update-task", json=payload)

def list_tasks(user_id):
    # Lists all tasks for a specific user
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def new_task_payload():
    # Builds a fresh task with unique content and user ID
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }
