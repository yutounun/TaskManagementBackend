from fastapi.testclient import TestClient
from starlette import status
from main import app
import pytest

client = TestClient(app)


LOGIN_DATA = {"username": "master", "password": "password"}
TASK_DATA = {
    "title": "test",
    "status": "test",
    "man_hour_min": 1,
    "to_date": "2023-08-14T15:32:00Z",
    "from_date": "2023-08-14T15:32:00Z",
    "priority": 1,
    "project_id": "test",
    "user_id": "test",
}
EDIT_TASK_DATA = {
    "title": "update test",
    "status": "update test",
    "man_hour_min": 2,
    "to_date": "2024-08-14T15:32:00Z",
    "from_date": "2024-08-14T15:32:00Z",
    "priority": 2,
    "project_id": "update test",
    "user_id": "update test",
}


@pytest.fixture
def headers():
    login_response = client.post("/auth/login/", data=LOGIN_DATA)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def created_task(headers):
    response = client.post("/tasks/", headers=headers, json=TASK_DATA)
    assert response.status_code == status.HTTP_200_OK
    yield response.json()  # return response

    # delete create data after each test
    # task_id = response.json()["id"]
    # del_response = client.delete("/tasks/" + task_id, headers=headers)
    # assert del_response.status_code == status.HTTP_200_OK


def extract_task_data(task):
    extract_data = {key: task[key] for key in TASK_DATA}
    extract_data["to_date"] = extract_data["to_date"] + "Z"
    extract_data["from_date"] = extract_data["from_date"] + "Z"
    return extract_data


def test_create_and_read(headers, created_task):
    task_id = created_task["id"]
    response = client.get("/tasks/" + task_id, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    obj_res = extract_task_data(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert obj_res == TASK_DATA

    response = client.get("/tasks/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    print("response.json()", response.json())


def test_edit_and_read(headers, created_task):
    task_id = created_task["id"]
    response = client.put("/tasks/" + task_id, headers=headers, json=EDIT_TASK_DATA)
    assert response.status_code == status.HTTP_200_OK

    obj_res = extract_task_data(response.json())
    assert obj_res == EDIT_TASK_DATA


def test_create_and_remove(headers, created_task):
    task_id = created_task["id"]
    response = client.delete("/tasks/" + task_id, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
