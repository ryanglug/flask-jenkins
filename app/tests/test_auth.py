import pytest
import tempfile
from app import app
from db import get_db
import os
import shutil


@pytest.fixture
def client():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test.db")

    app.config["DATABASE"] = db_path
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db = get_db()
            with open("schema.sql", "r") as f:
                db.executescript(f.read())
            db.commit()
        yield client

    shutil.rmtree(temp_dir)


def test_register(client):
    response = client.post("/register", json={"username": "user2", "password": "pass"})

    assert response.status_code == 204
