from app.config.database import VectorizedKnowledgeBase
from sqlalchemy.orm import Session
from app.schemas.knowledge_base import KnowledgeBaseCreate
from app.services.vectorize_service import text_to_vector


def get_all_knowledge_bases(db: Session):
    return db.query(VectorizedKnowledgeBase).all()

def create_knowledge_base(db: Session, knowledge_base: KnowledgeBaseCreate):
    vector = text_to_vector(knowledge_base.content)  # Преобразуем контент в вектор
    db_knowledge_base = VectorizedKnowledgeBase(title=knowledge_base.title, content=knowledge_base.content, vector=vector)
    db.add(db_knowledge_base)
    db.commit()
    db.refresh(db_knowledge_base)
    return db_knowledge_base