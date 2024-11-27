from flask import Blueprint, request, render_template_string
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