import tempfile

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBase
from app.repositories.knowledge_base_repository import get_knowledge_base_by_id, create_knowledge_base, \
    get_all_knowledge_bases
from app.services.together_service import search_together
from app.services.etl_service import process_txt_file, process_csv_file

router = APIRouter()


@router.post("/", response_model=KnowledgeBase)
def create_knowledge_base_entry(knowledge_base: KnowledgeBaseCreate, db: Session = Depends(get_db)):
    return create_knowledge_base(db=db, knowledge_base=knowledge_base)


@router.get("/{knowledge_base_id}", response_model=KnowledgeBase)
def read_knowledge_base_entry(knowledge_base_id: int, db: Session = Depends(get_db)):
    db_knowledge_base = get_knowledge_base_by_id(db, knowledge_base_id=knowledge_base_id)
    if db_knowledge_base is None:
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    return db_knowledge_base


@router.post("/upload-txt")
async def upload_txt_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.filename.endswith(".txt"):
        file_content = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        process_txt_file(temp_file_path, db)
        return {"message": "File processed successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .txt files are allowed.")


@router.post("/upload-csv")
async def upload_csv_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.filename.endswith(".csv"):
        file_content = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        process_csv_file(temp_file_path, db)
        return {"message": "File processed successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .csv files are allowed.")


@router.post("/search")
async def search_knowledge_base(query: str, template: str = Query(
    default="You are a helpful assistant. Data: {data}. User query: {query}"), db: Session = Depends(get_db)):
    # Получаем все записи из базы данных
    knowledge_bases = get_all_knowledge_bases(db)

    # Преобразуем записи в словарь
    data = {kb.id: {"title": kb.title, "content": kb.content} for kb in knowledge_bases}

    # Используем API Together для обработки запроса
    together_response = search_together(query, data, template)

    # Возвращаем структурированный ответ от Together
    return {"response": together_response}
