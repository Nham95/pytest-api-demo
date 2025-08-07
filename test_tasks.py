# test_tasks.py
import requests

BASE_URL = "https://todo.pixegami.io"

def test_can_create_task(create_task, new_task_payload):
    task_id = create_task["task_id"]

    # Fetch the task we just created
    response = requests.get(f"{BASE_URL}/get-task/{task_id}")
    assert response.status_code == 200


    # Check if the task data matches what we sent
    task_data = response.json()
    assert task_data["content"] == new_task_payload["content"]
    assert task_data["user_id"] == new_task_payload["user_id"]
    assert task_data["is_done"] == False

    #comparing the response with the payload that was sent


    print("✅ Task created and verified:", task_data)



# Test to update an existing task
def test_can_update_task(create_task):
    task_id = create_task["task_id"]
    user_id = create_task["user_id"]

    updated_payload = {
        "task_id": task_id,
        "user_id": user_id,
        "content": "Updated content from test",
        "is_done": True
    }

    # Send update
    update_response = requests.put(f"{BASE_URL}/update-task", json=updated_payload)
    assert update_response.status_code == 200

    # Fetch task
    get_response = requests.get(f"{BASE_URL}/get-task/{task_id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["content"] == "Updated content from test"
    assert data["is_done"] is True


