import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config.database import get_db
from app.repositories.knowledge_base_repository import create_knowledge_base
from app.schemas.knowledge_base import KnowledgeBaseCreate

client = TestClient(app)

@pytest.fixture(scope="function")
def populate_db(db_session):
    knowledge_base_entries = [
        KnowledgeBaseCreate(title="Test Title 1", content="Test Content 1"),
        KnowledgeBaseCreate(title="Test Title 2", content="Test Content 2"),
    ]
    for entry in knowledge_base_entries:
        create_knowledge_base(db_session, entry)
    yield

def test_search_knowledge_base(db_session, populate_db):
    app.dependency_overrides[get_db] = lambda: db_session
    query = "Какой контент содержит Test Title 1?"
    response = client.post(f"/knowledge-base/search?query={query}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "response" in response.json()
    # Additional assertions on response content
