import pytest
import tempfile
from app import app
from db_test import get_db, find_user
import os
import shutil

username = "user"
password = "pass"


@pytest.fixture
def client():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test.db")

    app.config["DATABASE"] = db_path
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db = get_db()
            with open("schema-tests.sql", "r") as f:
                db.executescript(f.read())
            db.commit()
        yield client

    shutil.rmtree(temp_dir)


@pytest.fixture
def create_user(client):
    response = client.post(
        "/api/register", json={"username": username, "password": password}
    )
    yield response


def test_register(create_user):
    # Creates the user
    assert create_user.status_code == 204

    # User now exists in the db
    user = find_user(username)

    assert user is not None


def test_invalid_register(client, create_user):
    # Missing body
    response = client.post("/api/register", json={"username": "", "password": password})

    assert response.status_code == 400

    # Missing password
    response = client.post("/api/register", json={"username": username, "password": ""})

    assert response.status_code == 400

    # Cannot create a user that already exists
    response = client.post(
        "/api/register", json={"username": username, "password": password}
    )

    assert response.status_code == 400

    assert response.get_json()["error"] == "Not allowed"


def test_login(client, create_user):
    # Access Token in body
    response = client.post(
        "/api/login",
        json={"username": username, "password": password},
    )

    assert response.status_code == 200

    access_token = response.get_json()["access"]

    assert access_token

    # Check that a cookie was returned
    assert "Set-Cookie" in response.headers

    cookie = response.headers.get("Set-Cookie")

    # Check the cookie is HttpOnly
    assert "HttpOnly" in cookie and "refresh_token" in cookie


def test_invalid_login(client, create_user):
    # Invalid password passed
    response = client.post(
        "/api/login",
        json={"username": username, "password": "wrong-pass"},
    )

    assert response.status_code == 400

    # Non existent user passed
    response = client.post(
        "/api/login",
        json={"username": "fake-user", "password": password},
    )

    assert response.status_code == 400


def test_create_comment(client, create_user):
    # Get the access token
    response = client.post(
        "/api/login",
        json={"username": username, "password": password},
    )

    access_token = response.get_json()["access"]

    assert access_token

    # Create a comment
    response = client.post(
        "/api/comment",
        json={"content": "Comment content"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    # Comment now exists in db


def test_invalid_create_comment(client, create_user):
    # Create with no auth
    response = client.post(
        "/api/comment",
        json={"content": "Comment content"},
    )

    assert response.status_code == 401

    # Create with invalid auth
    response = client.post(
        "/api/comment",
        json={"content": "Comment content"},
        headers={"Authorization": f"Bearer fake-token"},
    )

    assert response.status_code == 401

    # Valid auth but miss formatted request
    response = client.post(
        "/api/login",
        json={"username": username, "password": password},
    )

    access_token = response.get_json()["access"]

    assert access_token

    response = client.post(
        "/api/comment",
        json={"content": ""},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
