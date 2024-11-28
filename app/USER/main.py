import os
import tempfil

import chardet
import git
from atlassian import Confluence
from flask import Blueprint, request, render_template_string, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from langchain.document_transformers import html2text
from notion_client import Client
from urllib.parse import unquote
import requests

from app.DATABASE.services.vectorize_service import text_to_vector

main_bp = Blueprint('main', __name__)

# TODO : сделать так, чтобы url брался из env
DATABASE_PORT = "7471"
DATABASE_URL = f"http://database_api:{DATABASE_PORT}"


@main_bp.route('/', methods=['GET'])
def hello():
    return "Infina User"

@main_bp.route('/search', methods=['POST'])
@jwt_required()
def search():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Запрос на поиск в базу данных
    response = requests.post(f"{DATABASE_URL}/search", json={"query": query})
    return jsonify(response.json()), response.status_code