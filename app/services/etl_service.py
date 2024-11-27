from app.connectors.csv_connector import read_csv_file
from app.connectors.txt_connector import read_txt_file
from app.repositories.knowledge_base_repository import create_knowledge_base
from sqlalchemy.orm import Session
from app.schemas.knowledge_base import KnowledgeBaseCreate
from docx import Document
import openpyxl
import PyPDF2

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

def process_docx_file(file_path, db):
    doc = Document(file_path)
    content = "\n".join([para.text for para in doc.paragraphs])
    knowledge_base_entry = KnowledgeBaseCreate(
        title=file_path.split("/")[-1],
        content=content
    )
    create_knowledge_base(db, knowledge_base_entry)

def process_xlsx_file(file_path, db):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    content = "\n".join([f"{cell.value}" for row in sheet.iter_rows() for cell in row])
    knowledge_base_entry = KnowledgeBaseCreate(
        title=file_path.split("/")[-1],
        content=content
    )
    create_knowledge_base(db, knowledge_base_entry)

def process_pdf_file(file_path, db):
    pdf_reader = PyPDF2.PdfFileReader(file_path)
    content = "\n".join([pdf_reader.getPage(i).extract_text() for i in range(pdf_reader.numPages)])
    knowledge_base_entry = KnowledgeBaseCreate(
        title=file_path.split("/")[-1],
        content=content
    )
    create_knowledge_base(db, knowledge_base_entry)
