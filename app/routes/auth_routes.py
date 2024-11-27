from flask import jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.database import User


def register_user(request, session):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
        return jsonify({"message": "Email and password are required"}), 400

    print("Email: ", email)
    print("Password: ", password)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='scrypt')
    new_user = User(email=email, password=hashed_password, role=role)

    session.add(new_user)
    session.commit()

    return jsonify({"message": "User registered successfully"}), 201

def login_user(request, db):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token, "role": user.role}), 200
