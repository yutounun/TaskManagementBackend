from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status
from main import app

client = TestClient(app)


request_body = {
    "title": "test",
    "status": "test",
    "man_hour_min": 1,
    "to_date": "2023-08-14T15:32:00Z",
    "from_date": "2023-08-14T15:32:00Z",
    "priority": 1,
    "project_key": "test",
    "user_key": "test",
}


def login():
    login_response = client.post(
        "/auth/login/",
        data={"username": "yuto", "password": "password"},
    )
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_task():
    headers = login()
    create_response = client.post("/tasks/", headers=headers, json=request_body)
    assert create_response.status_code == status.HTTP_200_OK
    return create_response


def test_create_and_read():
    headers = login()
    create_response = create_task()

    task_id = create_response.json()["id"]
    response = client.get("/tasks/" + task_id, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    obj_res = response.json()
    obj_res = {
        "title": obj_res["title"],
        "status": obj_res["status"],
        "man_hour_min": obj_res["man_hour_min"],
        "to_date": obj_res["to_date"] + "Z",
        "from_date": obj_res["from_date"] + "Z",
        "priority": obj_res["priority"],
        "project_key": obj_res["project_key"],
        "user_key": obj_res["user_key"],
    }
    assert obj_res == request_body


def test_create_and_remove():
    headers = login()
    create_response = create_task()

    task_id = create_response.json()["id"]
    response = client.get("/tasks/" + task_id, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    obj_res = response.json()
    obj_res = {
        "title": obj_res["title"],
        "status": obj_res["status"],
        "man_hour_min": obj_res["man_hour_min"],
        "to_date": obj_res["to_date"] + "Z",
        "from_date": obj_res["from_date"] + "Z",
        "priority": obj_res["priority"],
        "project_key": obj_res["project_key"],
        "user_key": obj_res["user_key"],
    }
    assert obj_res == request_body
