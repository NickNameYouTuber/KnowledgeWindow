from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.create_app import db, jwt
from app.routes.knowledge_base_routes import upload_txt_file, upload_csv_file, search_knowledge_base
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

@main_bp.route('/search', methods=['POST'])
@jwt_required()
def search():
    print("Request: ", request.args)
    query = request.args.get('query')
    print("Query: ", query)
    template = request.args.get('template', default="Answer clearly. Answer only questions about data. Answer only in Russian. Data: {data}. User query: {query}")
    return search_knowledge_base(query, template, db.session)

@main_bp.route('/register', methods=['POST'])
def register():
    return register_user(request, db.session)

@main_bp.route('/login', methods=['POST'])
def login():
    return login_user(request, db.session)