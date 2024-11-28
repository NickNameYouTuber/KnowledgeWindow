import os
import tempfile

import chardet
import git
from atlassian import Confluence
from flask import Blueprint, request, render_template_string, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from langchain.document_transformers import html2text
from notion_client import Client

from app.DATABASE.config.database import UserQueryHistory, User, NeuralNetworkSettings, VectorizedKnowledgeBase, PromptTemplate
from app.create_app import db
from app.routes.knowledge_base_routes import upload_txt_file, upload_csv_file, upload_pdf_file, \
    upload_xlsx_file, upload_docx_file, upload_md_file
from app.routes.auth_routes import register_user, login_user
from urllib.parse import unquote

from app.DATABASE.services.vectorize_service import text_to_vector

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def hello():
    return "Hello World"

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

@main_bp.route('/embed', methods=['GET'])
def embed():
    # Get customization parameters from URL
    format_size = request.args.get('format', 'small')
    bg_color = unquote(request.args.get('color', '#ffffff'))
    theme = request.args.get('theme', 'light')
    border_radius = request.args.get('borderRadius', '8')
    font_size = request.args.get('fontSize', '14')
    button_color = unquote(request.args.get('buttonColor', '#3B82F6'))
    input_style = request.args.get('inputStyle', 'modern')
    animation_speed = request.args.get('animationSpeed', '300')

    # Calculate dimensions based on format
    padding = '24px' if format_size == 'full' else '16px'
    width = '100%' if format_size == 'full' else '400px'

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            :root {{
                --primary-color: {button_color};
                --bg-color: {bg_color};
                --animation-speed: {animation_speed}ms;
                --border-radius: {border_radius}px;
                --font-size: {font_size}px;
            }}

            * {{
                box-sizing: border-box;
                transition: all var(--animation-speed) ease;
            }}

            body {{
                background-color: var(--bg-color);
                padding: {padding};
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-size: var(--font-size);
                margin: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .container {{
                width: {width};
                max-width: 100%;
                background: {'#1F2937' if theme == 'dark' else '#ffffff'};
                color: {'#F9FAFB' if theme == 'dark' else '#111827'};
                border-radius: var(--border-radius);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                padding: {padding};
            }}

            .input-wrapper {{
                position: relative;
                margin-bottom: 1rem;
            }}

            .input-field {{
                width: 100%;
                padding: 0.75rem 1rem;
                border: {
    '1px solid #E5E7EB' if input_style == 'modern' else
    'none' if input_style == 'minimal' else
    '2px solid #E5E7EB'
    };
                border-radius: var(--border-radius);
                background: {
    '#374151' if theme == 'dark' else '#F9FAFB' if input_style == 'modern' else
    '#374151' if theme == 'dark' else '#ffffff' if input_style == 'minimal' else
    '#1F2937' if theme == 'dark' else '#F3F4F6'
                };
                outline: none;
                transition: all var(--animation-speed) ease;
            }}

            .input-field:focus {{
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }}

            .submit-button {{
                width: 100%;
                padding: 0.75rem 1rem;
                background: var(--primary-color);
                color: white;
                border: none;
                border-radius: var(--border-radius);
                cursor: pointer;
                font-weight: 500;
                transition: all var(--animation-speed) ease;
            }}

            .submit-button:hover {{
                opacity: 0.9;
                transform: translateY(-1px);
            }}

            .response-area {{
                margin-top: 1rem;
                padding: 1rem;
                border-radius: var(--border-radius);
                background: {'#374151' if theme == 'dark' else '#F9FAFB'};
                min-height: 100px;
                opacity: 0;
                transform: translateY(10px);
            }}

            .response-area.visible {{
                opacity: 1;
                transform: translateY(0);
            }}

            .loading {{
                display: none;
                justify-content: center;
                align-items: center;
                gap: 8px;
                margin-top: 1rem;
            }}

            .loading.visible {{
                display: flex;
            }}

            .loading-dot {{
                width: 8px;
                height: 8px;
                background: var(--primary-color);
                border-radius: 50%;
                animation: bounce var(--animation-speed) infinite ease-in-out;
            }}

            .loading-dot:nth-child(2) {{ animation-delay: 0.1s; }}
            .loading-dot:nth-child(3) {{ animation-delay: 0.2s; }}

            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-6px); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <form onsubmit="handleSubmit(event)" class="space-y-4">
                <div class="input-wrapper">
                    <input 
                        type="text" 
                        id="query" 
                        class="input-field"
                        placeholder="Enter your query..."
                        autocomplete="off"
                    />
                </div>
                <button type="submit" class="submit-button">
                    Search
                </button>
            </form>

            <div class="loading">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>

            <div id="response" class="response-area"></div>
        </div>

        <script>
            const loading = document.querySelector('.loading');
            const responseArea = document.querySelector('.response-area');

            async function handleSubmit(event) {{
                event.preventDefault();
                const query = document.getElementById('query').value;

                if (!query.trim()) return;

                loading.classList.add('visible');
                responseArea.classList.remove('visible');
                responseArea.innerText = '';

                try {{
                    const res = await fetch('http://127.0.0.1:5000/search?query=' + encodeURIComponent(query), {{
                        method: 'POST'
                    }});

                    const data = await res.json();

                    loading.classList.remove('visible');
                    responseArea.innerText = data.response;
                    responseArea.classList.add('visible');
                }} catch (error) {{
                    loading.classList.remove('visible');
                    responseArea.innerText = 'Error: Could not fetch response. Please try again.';
                    responseArea.classList.add('visible');
                    console.error("Error fetching data:", error);
                }}
            }}
        </script>
    </body>
    </html>
    """

    return render_template_string(html)

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