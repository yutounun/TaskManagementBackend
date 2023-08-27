from fastapi.testclient import TestClient
from starlette import status
from main import app
import pytest

client = TestClient(app)


LOGIN_DATA = {"username": "master", "password": "password"}
PROJECT_DATA = {
    "title": "test",
    "status": "test",
    "total_man_hour_min": 1,
    "to_date": "2023-08-14T15:32:00Z",
    "from_date": "2023-08-14T15:32:00Z",
    "user_key": "test",
}
EDIT_PROJECT_DATA = {
    "title": "update test",
    "status": "update test",
    "total_man_hour_min": 2,
    "to_date": "2024-08-14T15:32:00Z",
    "from_date": "2024-08-14T15:32:00Z",
    "user_key": "test",
}


@pytest.fixture
def headers():
    login_response = client.post("/auth/login/", data=LOGIN_DATA)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def created_project(headers):
    response = client.post("/projects/", headers=headers, json=PROJECT_DATA)
    print("response.json()1", response.json())
    assert response.status_code == status.HTTP_200_OK
    yield response.json()  # return response

    # delete create data after each test
    # project_id = response.json()["id"]
    # print("project_id: ", project_id)
    # del_response = client.delete("/projects/" + project_id, headers=headers)
    # assert del_response.status_code == status.HTTP_200_OK


def extract_PROJECT_data(project):
    extract_data = {key: project[key] for key in PROJECT_DATA}
    extract_data["to_date"] = extract_data["to_date"] + "Z"
    extract_data["from_date"] = extract_data["from_date"] + "Z"
    return extract_data


def test_create_and_read(headers, created_project):
    project_id = created_project["id"]
    response = client.get("/projects/" + project_id, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    obj_res = extract_PROJECT_data(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert obj_res == PROJECT_DATA

    response = client.get("/projects/", headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_edit_and_read(headers, created_project):
    project_id = created_project["id"]
    print("project_id1: ", project_id)

    response = client.put(
        "/projects/" + project_id, headers=headers, json=EDIT_PROJECT_DATA
    )
    assert response.status_code == status.HTTP_200_OK

    obj_res = extract_PROJECT_data(response.json())
    assert obj_res == EDIT_PROJECT_DATA


def test_create_and_remove(headers, created_project):
    project_id = created_project["id"]
    response = client.delete("/projects/" + project_id, headers=headers)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
