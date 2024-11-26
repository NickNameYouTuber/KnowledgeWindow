from app.connectors.csv_connector import read_csv_file
from app.connectors.txt_connector import read_txt_file
from app.repositories.knowledge_base_repository import create_knowledge_base
from sqlalchemy.orm import Session
from app.schemas.knowledge_base import KnowledgeBaseCreate

def process_txt_file(file_path: str, db: Session):
    """
    Обрабатывает .txt файл, создавая запись в базе знаний.
    """
    content = read_txt_file(file_path)
    knowledge_base_entry = KnowledgeBaseCreate(
        title=file_path.split("/")[-1],
        content=content
    )
    create_knowledge_base(db, knowledge_base_entry)

def process_csv_file(file_path: str, db: Session):
    """
    Обрабатывает .csv файл, создавая запись в базе знаний.
    """
    df = read_csv_file(file_path)
    content = df.to_string(index=False)
    knowledge_base_entry = KnowledgeBaseCreate(
        title=file_path.split("/")[-1],
        content=content
    )
    create_knowledge_base(db, knowledge_base_entry)