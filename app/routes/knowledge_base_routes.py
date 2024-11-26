from flask import request, jsonify
from werkzeug.utils import secure_filename
from app.services.etl_service import process_txt_file, process_csv_file
from app.services.together_service import search_together
from app.repositories.knowledge_base_repository import get_all_knowledge_bases
import tempfile


def upload_txt_file(request, db):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename.endswith(".txt"):
        file_content = file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        process_txt_file(temp_file_path, db)
        return jsonify({"message": "File processed successfully"})
    else:
        return jsonify({"error": "Invalid file type. Only .txt files are allowed."}), 400


def upload_csv_file(request, db):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename.endswith(".csv"):
        file_content = file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        process_csv_file(temp_file_path, db)
        return jsonify({"message": "File processed successfully"})
    else:
        return jsonify({"error": "Invalid file type. Only .csv files are allowed."}), 400


def search_knowledge_base(query, template, db):
    # Получаем все записи из базы данных
    # knowledge_bases = get_all_knowledge_bases(db)

    # Преобразуем записи в словарь
    # data = {kb.id: {"title": kb.title, "content": kb.content} for kb in knowledge_bases}
    data = {
        1: {"title": "Test Title 1", "content": "Test Content 1"},
        2: {"title": "Test Title 2", "content": "Test Content 2"},}

    # Используем API Together для обработки запроса
    together_response = search_together(query, data, template)

    # Возвращаем структурированный ответ от Together
    return jsonify({"response": together_response})