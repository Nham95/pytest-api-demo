import requests

ENDPOINT = "https://todo.pixegami.io/"

def test_can_call_endpoint(): # this is a simple test to check if the endpoint is reachable
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task(): #this test checks if we can create a task
    payload = { # this is the payload we will send to the endpoint
        "content": "test content",
        "user_id": "test_user",
        "is_done": False
    }
            # a payload is a dictionary that contains the data we want to send to the endpoint
    
    create_task_response = requests.put(ENDPOINT+"/create-task", json=payload) 
    # this sends a PUT request to the endpoint with the payload as JSON
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    # Check if the task was created successfully

    task_id = data["task"]["task_id"]
    get_task_response = requests.get(ENDPOINT+ f"/get-task/{task_id}")
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == "test content"
    assert get_task_data["user_id"] == payload["user_id"]
    print(get_task_data)
    # Check if the task data matches the payload we sent
