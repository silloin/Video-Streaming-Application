from flask import Blueprint, request, jsonify, current_app
from extensions import mongo
from models import User
import jwt
import datetime
import bcrypt
from bson.objectid import ObjectId

auth_bp = Blueprint("auth", __name__)

def generate_token(user_id):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
        "sub": str(user_id)
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User.create(name, email, password_hash)
    
    result = mongo.db.users.insert_one(user)
    
    token = generate_token(result.inserted_id)
    
    return jsonify({
        "message": "User created",
        "token": token,
        "user": {"id": str(result.inserted_id), "name": name, "email": email}
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user["password_hash"]):
        token = generate_token(user["_id"])
        return jsonify({
            "token": token,
            "user": {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/me", methods=["GET"])
def me():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing token"}), 401
    
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
        user_id = payload["sub"]
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        })
    except (jwt.InvalidTokenError, jwt.DecodeError, IndexError):
        return jsonify({"error": "Invalid token"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out"}), 200
