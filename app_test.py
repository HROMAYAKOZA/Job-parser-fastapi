import pytest
from src.parse_hh import hhru_parse_job, hhru_parse_resum
from fastapi.testclient import TestClient
from main import app

def test_parsers():
    assert hhru_parse_job("https://hh.ru/search/vacancy?text=&area=1/") != []
    assert hhru_parse_resum(
        "https://hh.ru/search/resume?text=&area=1&items_on_page=100") != []


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_bd_actions(client):
    response = client.get("/jobs")
    assert response.status_code == 200
    assert response.json() != []
    response = client.get("/resums")
    assert response.status_code == 200
    assert response.json() != []


def test_filters(client):
    response = client.post(
        "/jobs_f",
        json={
            "salary": "0",
            "city": "",
            "experience": "0",
            "remote": "false",
            "req_resume": "false",
        },
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200
    assert response.json() != []
    response = client.post(
        "/resums_f",
        json={"max_salary": "9999999", "experience": "0", "status": "false"},
    )
    assert response.status_code == 200
    assert response.json() != []
