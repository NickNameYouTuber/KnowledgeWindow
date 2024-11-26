from sqlalchemy.orm import Session
from app.models.knowledge_base import KnowledgeBase
from app.schemas.knowledge_base import KnowledgeBaseCreate

def get_knowledge_base_by_id(db: Session, knowledge_base_id: int):
    return db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()

def create_knowledge_base(db: Session, knowledge_base: KnowledgeBaseCreate):
    db_knowledge_base = KnowledgeBase(title=knowledge_base.title, content=knowledge_base.content)
    db.add(db_knowledge_base)
    db.commit()
    db.refresh(db_knowledge_base)
    return db_knowledge_base

def get_all_knowledge_bases(db: Session):
    return db.query(KnowledgeBase).all()