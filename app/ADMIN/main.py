from flask import Blueprint, request, render_template_string, jsonify
from flask_jwt_extended import jwt_required
from create_app import db
from urllib.parse import unquote

# Основной Blueprint
main_bp = Blueprint('main', __name__)

# Под-Blueprint для embed
embed_bp = Blueprint('embed', __name__)

@embed_bp.route('/', methods=['GET'])
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

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload-txt', methods=['POST'])
@jwt_required()
def upload_txt():
    pass

@upload_bp.route('/upload-pdf', methods=['POST'])
@jwt_required()
def upload_pdf():
    pass

@upload_bp.route('/upload-docx', methods=['POST'])
@jwt_required()
def upload_docx():
    pass

@upload_bp.route('/upload-xlsx', methods=['POST'])
@jwt_required()
def upload_xlsx():
    pass

@upload_bp.route('/upload-md', methods=['POST'])
@jwt_required()
def upload_md():
    pass

@upload_bp.route('/upload-repo', methods=['POST'])
@jwt_required()
def upload_repo():
    pass

@upload_bp.route('/upload-csv', methods=['POST'])
@jwt_required()
def upload_csv():
    pass

@upload_bp.route('/upload-confluence', methods=['POST'])
@jwt_required()
def upload_confluence():
    pass

@upload_bp.route('/upload-notion', methods=['POST'])
@jwt_required()
def upload_notion():
    pass

# Под-Blueprint для neural_network
neural_network_bp = Blueprint('neural_network', __name__)

@neural_network_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    # TODO: Сделать запрос на получение настроек
    settings = ...
    if not settings:
        return jsonify({"error": "Settings not found"}), 404
    return jsonify({
        "url": settings.url,
        "api_key": settings.api_key,
        "model": settings.model
    })

@neural_network_bp.route('/settings', methods=['POST'])
@jwt_required()
def create_settings():
    data = request.json
    if not data or not data.get('url') or not data.get('api_key') or not data.get('model'):
        return jsonify({"error": "Missing required fields"}), 400

    # TODO: Сделать запрос на создание настроек
    settings = ...
    db.session.add(settings)
    db.session.commit()
    return jsonify({"message": "Settings created successfully"})

@neural_network_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    data = request.json
    if not data or not data.get('url') or not data.get('api_key') or not data.get('model'):
        return jsonify({"error": "Missing required fields"}), 400

    # TODO: Сделать запрос на обновление настроек
    settings =  ...
    if not settings:
        return jsonify({"error": "Settings not found"}), 404

    settings.url = data['url']
    settings.api_key = data['api_key']
    settings.model = data['model']
    db.session.commit()
    return jsonify({"message": "Settings updated successfully"})

# Под-Blueprint для files
files_bp = Blueprint('files', __name__)

@files_bp.route('/', methods=['GET'])
@jwt_required()
def get_files():
    # TODO: Сделать запрос на получение файлов
    files = ...
    return jsonify([{
        "id": file.id,
        "title": file.title,
        "content": file.content
    } for file in files])

@files_bp.route('/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    # TODO: Сделать запрос на удаление файла
    file = ...
    if not file:
        return jsonify({"error": "File not found"}), 404
    db.session.delete(file)
    db.session.commit()
    return jsonify({"message": "File deleted successfully"})

# Под-Blueprint для prompt_template
prompt_template_bp = Blueprint('prompt_template', __name__)

@prompt_template_bp.route('/', methods=['GET'])
@jwt_required()
def get_prompt_template():
    # TODO: Сделать запрос на получение шаблона
    template = ...
    if not template:
        return jsonify({"error": "Template not found"}), 404
    return jsonify({
        "id": template.id,
        "name": template.name,
        "content": template.content
    })

@prompt_template_bp.route('/', methods=['PUT'])
@jwt_required()
def update_prompt_template():
    data = request.json
    if not data or not data.get('content'):
        return jsonify({"error": "Missing required fields"}), 400

    # TODO: Сделать запрос на обновление шаблона
    template = ...
    if not template:
        return jsonify({"error": "Template not found"}), 404

    template.content = data['content']
    db.session.commit()
    return jsonify({"message": "Template updated successfully"})

# Регистрация под-Blueprint'ов в основном Blueprint'е
main_bp.register_blueprint(embed_bp, url_prefix='/embed')
main_bp.register_blueprint(neural_network_bp, url_prefix='/neural-network')
main_bp.register_blueprint(files_bp, url_prefix='/files')
main_bp.register_blueprint(prompt_template_bp, url_prefix='/prompt-template')
main_bp.register_blueprint(upload_bp, url_prefix='/upload')

# Добавление маршрута для приветствия
@main_bp.route('/', methods=['GET'])
def hello():
    return "Infina"