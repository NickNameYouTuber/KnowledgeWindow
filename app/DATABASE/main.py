import os
import tempfile

import chardet
import git
from atlassian import Confluence
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from langchain.document_transformers import html2text
from notion_client import Client

from app.DATABASE.config.database import UserQueryHistory, User, NeuralNetworkSettings, VectorizedKnowledgeBase, PromptTemplate
from app.create_app import db
from app.routes.knowledge_base_routes import upload_txt_file, upload_csv_file, upload_pdf_file, \
    upload_xlsx_file, upload_docx_file, upload_md_file
from app.routes.auth_routes import register_user, login_user

from app.DATABASE.services.vectorize_service import text_to_vector

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def hello():
    return "Infina Database"

@main_bp.route('/upload-txt', methods=['POST'])
@jwt_required()
def upload_txt():
    return upload_txt_file(request, db)

@main_bp.route('/upload-csv', methods=['POST'])
@jwt_required()
def upload_csv():
    return upload_csv_file(request, db)

@main_bp.route('/upload-docx', methods=['POST'])
@jwt_required()
def upload_docx():
    return upload_docx_file(request, db)

@main_bp.route('/upload-xlsx', methods=['POST'])
@jwt_required()
def upload_xlsx():
    return upload_xlsx_file(request, db)

@main_bp.route('/upload-pdf', methods=['POST'])
@jwt_required()
def upload_pdf():
    return upload_pdf_file(request, db)

@main_bp.route('/upload-md', methods=['POST'])
@jwt_required()
def upload_md():
    return upload_md_file(request, db)

@main_bp.route('/upload-repo', methods=['POST'])
@jwt_required()
def upload_repo():
    repo_url = request.json.get('repo_url')
    if not repo_url:
        return jsonify({"error": "No repository URL provided"}), 400

    try:
        # Создаем временную директорию для клонирования репозитория
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Клонируем репозиторий во временную директорию
            git.Repo.clone_from(repo_url, tmpdirname)

            # Проходим по всем файлам в репозитории
            for root, dirs, files in os.walk(tmpdirname):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()

                    # Определяем кодировку файла
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']

                    # Если кодировка не определена, используем UTF-8 по умолчанию
                    if encoding is None:
                        encoding = 'utf-8'

                    # Читаем файл с правильной кодировкой
                    file_content = raw_data.decode(encoding, errors='ignore')

                    # Определяем тип файла по расширению
                    file_extension = file.split('.')[-1].lower()
                    if file_extension in ['txt', 'csv', 'docx', 'xlsx', 'pdf', 'md']:
                        vector = text_to_vector(file_content)
                        new_entry = VectorizedKnowledgeBase(title=file, content=file_content, vector=vector)
                        db.session.add(new_entry)

            db.session.commit()
            return jsonify({"message": "Repository processed and files added successfully"})

    except Exception as e:
        db.session.rollback()
        print(f"Error processing repository: {str(e)}")
        return jsonify({"error": str(e)}), 500


@main_bp.route('/upload-confluence', methods=['POST'])
@jwt_required()
def upload_confluence():
    try:
        data = request.json
        workspace_url = data.get('workspace_url')
        api_key = data.get('api_key')
        space_key = data.get('space_key')

        if not all([workspace_url, api_key, space_key]):
            return jsonify({"error": "Missing required fields"}), 400

        # Инициализация клиента Confluence
        confluence = Confluence(
            url=workspace_url,
            token=api_key
        )

        # Получение всех страниц из указанного пространства
        pages = confluence.get_all_pages_from_space(space_key, start=0, limit=500)

        # HTML в текст конвертер
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True

        for page in pages:
            try:
                # Получение содержимого страницы
                page_content = confluence.get_page_by_id(page['id'], expand='body.storage')
                html_content = page_content['body']['storage']['value']

                # Конвертация HTML в текст
                text_content = h.handle(html_content)

                # Создание вектора из текста
                vector = text_to_vector(text_content)

                # Сохранение в базу данных
                new_entry = VectorizedKnowledgeBase(
                    title=page['title'],
                    content=text_content,
                    vector=vector,
                    source='confluence',
                    metadata={
                        'page_id': page['id'],
                        'space_key': space_key,
                        'url': f"{workspace_url}/wiki/spaces/{space_key}/pages/{page['id']}"
                    }
                )
                db.session.add(new_entry)

            except Exception as e:
                print(f"Error processing page {page['title']}: {str(e)}")
                continue

        db.session.commit()
        return jsonify({"message": f"Successfully processed {len(pages)} Confluence pages"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main_bp.route('/upload-notion', methods=['POST'])
@jwt_required()
def upload_notion():
    try:
        data = request.json
        api_key = data.get('api_key')
        workspace_url = data.get('workspace_url')

        if not api_key:
            return jsonify({"error": "Missing API key"}), 400

        # Инициализация клиента Notion
        notion = Client(auth=api_key)

        # Получение списка всех страниц
        response = notion.search()

        for page in response['results']:
            try:
                if page['object'] != 'page':
                    continue

                # Получение содержимого страницы
                page_content = notion.blocks.children.list(page['id'])

                # Извлечение текста из блоков
                text_content = ""
                for block in page_content['results']:
                    if block['type'] == 'paragraph' and 'text' in block['paragraph']:
                        for text in block['paragraph']['text']:
                            if 'plain_text' in text:
                                text_content += text['plain_text'] + "\n"
                    elif block['type'] == 'heading_1' and 'text' in block['heading_1']:
                        for text in block['heading_1']['text']:
                            if 'plain_text' in text:
                                text_content += "# " + text['plain_text'] + "\n"
                    elif block['type'] == 'heading_2' and 'text' in block['heading_2']:
                        for text in block['heading_2']['text']:
                            if 'plain_text' in text:
                                text_content += "## " + text['plain_text'] + "\n"
                    elif block['type'] == 'heading_3' and 'text' in block['heading_3']:
                        for text in block['heading_3']['text']:
                            if 'plain_text' in text:
                                text_content += "### " + text['plain_text'] + "\n"

                # Создание вектора из текста
                if text_content:
                    vector = text_to_vector(text_content)

                    # Сохранение в базу данных
                    new_entry = VectorizedKnowledgeBase(
                        title=page.get('properties', {}).get('title', [{}])[0].get('text', {}).get('content',
                                                                                                   'Untitled'),
                        content=text_content,
                        vector=vector,
                        source='notion',
                        metadata={
                            'page_id': page['id'],
                            'url': page['url'] if 'url' in page else workspace_url
                        }
                    )
                    db.session.add(new_entry)

            except Exception as e:
                print(f"Error processing Notion page {page.get('id')}: {str(e)}")
                continue

        db.session.commit()
        return jsonify({"message": f"Successfully processed Notion workspace content"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Вспомогательный маршрут для получения списка документов по источнику
@main_bp.route('/documents/<source>', methods=['GET'])
@jwt_required()
def get_documents_by_source(source):
    try:
        documents = VectorizedKnowledgeBase.query.filter_by(source=source).all()
        return jsonify([{
            'id': doc.id,
            'title': doc.title,
            'source': doc.source,
            'metadata': doc.metadata,
            'created_at': doc.created_at.isoformat()
        } for doc in documents])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Маршрут для удаления документа
@main_bp.route('/documents/<int:doc_id>', methods=['DELETE'])
@jwt_required()
def delete_document(doc_id):
    try:
        document = VectorizedKnowledgeBase.query.get(doc_id)
        if not document:
            return jsonify({"error": "Document not found"}), 404

        db.session.delete(document)
        db.session.commit()
        return jsonify({"message": "Document deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    # Get current user by email
    current_user_email = get_jwt_identity()
    print(current_user_email)
    current_user = db.session.query(User).filter_by(email=current_user_email).first()

    if not current_user:
        return jsonify({"error": "User not found"}), 404

    # Get user's query history
    history = db.session.query(UserQueryHistory).filter_by(user_id=current_user.id)\
        .order_by(UserQueryHistory.timestamp.desc()).all()

    return jsonify([{
        'query': item.query,
        'response': item.response,
        'timestamp': item.timestamp.isoformat()
    } for item in history])

@main_bp.route('/register', methods=['POST'])
def register():
    return register_user(request, db.session)

@main_bp.route('/login', methods=['POST'])
def login():
    return login_user(request, db.session)

@main_bp.route('/neural-network/settings', methods=['GET'])
@jwt_required()
def get_settings():
    settings = NeuralNetworkSettings.query.first()
    if not settings:
        return jsonify({"error": "Settings not found"}), 404
    return jsonify({
        "url": settings.url,
        "api_key": settings.api_key,
        "model": settings.model
    })

@main_bp.route('/neural-network/settings', methods=['POST'])
@jwt_required()
def create_settings():
    data = request.json
    if not data or not data.get('url') or not data.get('api_key') or not data.get('model'):
        return jsonify({"error": "Missing required fields"}), 400

    settings = NeuralNetworkSettings(
        url=data['url'],
        api_key=data['api_key'],
        model=data['model']
    )
    db.session.add(settings)
    db.session.commit()
    return jsonify({"message": "Settings created successfully"})

@main_bp.route('/neural-network/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    data = request.json
    if not data or not data.get('url') or not data.get('api_key') or not data.get('model'):
        return jsonify({"error": "Missing required fields"}), 400

    settings = NeuralNetworkSettings.query.first()
    if not settings:
        return jsonify({"error": "Settings not found"}), 404

    settings.url = data['url']
    settings.api_key = data['api_key']
    settings.model = data['model']
    db.session.commit()
    return jsonify({"message": "Settings updated successfully"})

@main_bp.route('/files', methods=['GET'])
@jwt_required()
def get_files():
    files = VectorizedKnowledgeBase.query.all()
    return jsonify([{
        "id": file.id,
        "title": file.title,
        "content": file.content
    } for file in files])

@main_bp.route('/files/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    file = VectorizedKnowledgeBase.query.get(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404
    db.session.delete(file)
    db.session.commit()
    return jsonify({"message": "File deleted successfully"})

@main_bp.route('/prompt-template', methods=['GET'])
@jwt_required()
def get_prompt_template():
    template = PromptTemplate.query.first()
    if not template:
        return jsonify({"error": "Template not found"}), 404
    return jsonify({
        "id": template.id,
        "name": template.name,
        "content": template.content
    })

@main_bp.route('/prompt-template', methods=['PUT'])
@jwt_required()
def update_prompt_template():
    data = request.json
    if not data or not data.get('content'):
        return jsonify({"error": "Missing required fields"}), 400

    template = PromptTemplate.query.first()
    if not template:
        return jsonify({"error": "Template not found"}), 404

    template.content = data['content']
    db.session.commit()
    return jsonify({"message": "Template updated successfully"})

@main_bp.route('/search', methods=['POST'])
def search():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({"error": "No query provided"}), 400

        template = request.args.get('template',
                                    default="Answer clearly. Answer only questions about data. Answer only in Russian. Data: {data}. User query: {query}")

        # Search knowledge base
        response_data = search_knowledge_base(query, template, db)

        # Get current user
        current_user_email = "123ababab123ababab@gmail.com"  # !FOR TEST!
        current_user = User.query.filter_by(email=current_user_email).first()

        if not current_user:
            return jsonify({"error": "User not found"}), 404

        # Save query history
        new_history = UserQueryHistory(
            user_id=current_user.id,
            query=query,
            response=response_data['response']
        )
        db.session.add(new_history)
        db.session.commit()

        return jsonify(response_data)

    except Exception as e:
        db.session.rollback()
        print(f"Error in search route: {str(e)}")
        return jsonify({"error": str(e)}), 500