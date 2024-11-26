import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config.database import get_db
import tempfile

client = TestClient(app)

@pytest.fixture(scope="module")
def test_txt_file():
    content = """
    Title: Пример текстового файла

    Это пример текстового файла, который может быть использован для тестирования вашего коннектора и маршрута.

    Содержимое файла может включать в себя:
    - Текст
    - Абзацы
    - Списки
    - Другие элементы текстового формата

    Надеюсь, этот пример будет полезен для ваших тестов!
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(content.encode("utf-8"))
        temp_file_path = temp_file.name
    yield temp_file_path
    import os
    os.remove(temp_file_path)

def test_upload_txt_file(test_txt_file, db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with open(test_txt_file, "rb") as file:
        response = client.post(
            "/knowledge-base/upload-txt",
            files={"file": ("test_example.txt", file, "text/plain")}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "File processed successfully"}

    # Проверка, что запись была создана в базе данных
    response = client.get("/knowledge-base/1")
    assert response.status_code == 200
    assert "Пример текстового файла" in response.json()["content"]