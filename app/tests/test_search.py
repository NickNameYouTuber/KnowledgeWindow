import pytest
from flask.testing import FlaskClient
from app.main import app
from app.config.database import get_db
from app.repositories.knowledge_base_repository import create_knowledge_base
from app.schemas.knowledge_base import KnowledgeBaseCreate

@pytest.fixture(scope="function")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def populate_db(db_session):
    knowledge_base_entries = [
        KnowledgeBaseCreate(title="Test Title 1", content="Test Content 1"),
        KnowledgeBaseCreate(title="Test Title 2", content="Test Content 2"),
    ]
    for entry in knowledge_base_entries:
        create_knowledge_base(db_session, entry)
    yield

def test_search_knowledge_base(client, populate_db):
    query = "Какой контент содержит Test Title 1?"
    template = "Answer clearly. Data: {data}. User query: {query}"
    response = client.post(f"/search?query={query}&template={template}")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert "response" in response.json
    # Additional assertions on response content