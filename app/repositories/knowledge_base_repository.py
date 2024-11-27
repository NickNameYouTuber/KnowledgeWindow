from app.config.database import KnowledgeBase
from sqlalchemy.orm import Session
from app.schemas.knowledge_base import KnowledgeBaseCreate

def get_all_knowledge_bases(db: Session):
    return db.query(KnowledgeBase).all()

def create_knowledge_base(db: Session, knowledge_base: KnowledgeBaseCreate):
    db_knowledge_base = KnowledgeBase(title=knowledge_base.title, content=knowledge_base.content)
    db.add(db_knowledge_base)
    db.commit()
    db.refresh(db_knowledge_base)
    return db_knowledge_base