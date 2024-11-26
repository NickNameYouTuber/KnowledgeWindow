import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config.database import get_db
import tempfile

client = TestClient(app)

@pytest.fixture(scope="module")
def test_csv_file():
    content = """
    Name,Age,City
    Alice,30,New York
    Bob,25,Los Angeles
    Charlie,35,Chicago
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(content.encode("utf-8"))
        temp_file_path = temp_file.name
    yield temp_file_path
    import os
    os.remove(temp_file_path)

def test_upload_csv_file(test_csv_file, db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with open(test_csv_file, "rb") as file:
        response = client.post(
            "/knowledge-base/upload-csv",
            files={"file": ("test_csv.csv", file, "text/csv")}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "File processed successfully"}

    # Проверка, что запись была создана в базе данных
    response = client.get("/knowledge-base/1")
    assert response.status_code == 200
    assert "Alice" in response.json()["content"]
    assert "Bob" in response.json()["content"]
    assert "Charlie" in response.json()["content"]