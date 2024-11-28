import os
import tempfile

import chardet
import git
from atlassian import Confluence
from flask import Blueprint, request, render_template_string, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from langchain.document_transformers import html2text
from notion_client import Client
from urllib.parse import unquote

from app.DATABASE.services.vectorize_service import text_to_vector

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def hello():
    return "Infina User"

@main_bp.route('/search', methods=['POST'])
@jwt_required()
def search():
    # TODO: Сделать запрос на поиск в базу данных
    pass