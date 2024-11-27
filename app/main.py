from flask import Blueprint, request, render_template_string, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.config.database import UserQueryHistory, User, NeuralNetworkSettings
from app.create_app import db, jwt
from app.routes.knowledge_base_routes import upload_txt_file, upload_csv_file, search_knowledge_base, upload_pdf_file, \
    upload_xlsx_file, upload_docx_file
from app.routes.auth_routes import register_user, login_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def hello():
    return "Hello World"

@main_bp.route('/upload-txt', methods=['POST'])
@jwt_required()
def upload_txt():
    return upload_txt_file(request, db.session)

@main_bp.route('/upload-csv', methods=['POST'])
@jwt_required()
def upload_csv():
    return upload_csv_file(request, db.session)

@main_bp.route('/upload-docx', methods=['POST'])
@jwt_required()
def upload_docx():
    return upload_docx_file(request, db.session)

@main_bp.route('/upload-xlsx', methods=['POST'])
@jwt_required()
def upload_xlsx():
    return upload_xlsx_file(request, db.session)

@main_bp.route('/upload-pdf', methods=['POST'])
@jwt_required()
def upload_pdf():
    return upload_pdf_file(request, db.session)

@main_bp.route('/search', methods=['POST'])
@jwt_required()
def search():
    query = request.args.get('query')
    template = request.args.get('template',
                                default="Answer clearly. Answer only questions about data. Answer only in Russian. Data: {data}. User query: {query}")

    # Здесь выполняется поиск в базе знаний и получение ответа
    response_data = search_knowledge_base(query, template, db.session)

    # Получаем текущего пользователя по email
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()

    if not current_user:
        return jsonify({"error": "User not found"}), 404

    # Сохраняем историю запроса
    new_history = UserQueryHistory(
        user_id=current_user.id,
        query=query,
        response=response_data['response']
    )
    db.session.add(new_history)
    db.session.commit()

    return jsonify(response_data)

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
    format = request.args.get('format', 'small')
    color = request.args.get('color', '#ffffff')

    padding = '20px' if format == 'full' else '10px'
    width = '100%' if format == 'full' else '300px'

    html = f"""
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: {color};
                padding: {padding};
                border-radius: 5px;
                width: {width};
                margin: auto;
            }}
        </style>
    </head>
    <body class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <form onsubmit="handleSubmit(event)" class="space-y-2">
            <input type="text" id="query" placeholder="Enter your query" class="border p-2 w-full" />
            <button type="submit" class="bg-blue-500 text-white p-2">Submit</button>
        </form>
        <div id="response" class="border p-2 mt-4"></div>
        <script>
            async function handleSubmit(event) {{
                event.preventDefault();
                const query = document.getElementById('query').value;
                const responseDiv = document.getElementById('response');
                try {{
                    const res = await fetch('http://127.0.0.1:5000/search?query=' + encodeURIComponent(query), {{
                        method: 'POST'
                    }});
                    const data = await res.json();
                    responseDiv.innerText = data.response;
                }} catch (error) {{
                    console.error("Error fetching data: ", error);
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