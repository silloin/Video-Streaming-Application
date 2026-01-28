from flask import Blueprint, request, jsonify, current_app, render_template_string
from extensions import mongo
from bson.objectid import ObjectId
import jwt
import datetime
import os
from models import Video

api_bp = Blueprint("api", __name__)

VIDEO_PLAYBACK_SECRET = os.getenv("VIDEO_PLAYBACK_SECRET", "video_playback_secret_key") # Separate secret for playback tokens

def verify_jwt(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
        return payload["sub"]
    except (jwt.InvalidTokenError, jwt.DecodeError, IndexError):
        return None

@api_bp.route("/dashboard", methods=["GET"])
def dashboard():
    # In a real app, verify JWT here. For dashboard, we might allow public or require auth.
    # Requirement: "Returns 2 video tiles fetched from backend"
    
    # Let's seed some data if empty
    if mongo.db.videos.count_documents({}) == 0:
        v1 = Video.create(
            "How Startups Fail", 
            "Lessons from real founders", 
            "bJzb-RuUcMU", # Example ID
            "https://img.youtube.com/vi/bJzb-RuUcMU/mqdefault.jpg"
        )
        v2 = Video.create(
            "The Art of Code", 
            "Beautiful programming", 
            "6avJHaC3C2U", 
            "https://img.youtube.com/vi/6avJHaC3C2U/mqdefault.jpg"
        )
        mongo.db.videos.insert_many([v1, v2])

    videos = mongo.db.videos.find({"is_active": True}).limit(2)
    result = []
    for v in videos:
        result.append({
            "id": str(v["_id"]),
            "title": v["title"],
            "description": v["description"],
            "thumbnail_url": v["thumbnail_url"]
            # NO youtube_id here
        })
    
    return jsonify(result)

@api_bp.route("/video/<id>/stream", methods=["GET"])
def get_stream(id):
    user_id = verify_jwt(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    video = mongo.db.videos.find_one({"_id": ObjectId(id)})
    if not video:
        return jsonify({"error": "Video not found"}), 404

    # Generate a short-lived playback token
    payload = {
        "video_id": video["youtube_id"], # We'll encode the real ID in the token
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }
    token = jwt.encode(payload, VIDEO_PLAYBACK_SECRET, algorithm="HS256")
    
    # Return the URL to our own player
    # Assuming the app is running on localhost:5000 accessible from emulator via 10.0.2.2 or IP
    # We will use relative path or configured host
    # For now, let's construct a full URL.
    # Note: Android Emulator uses 10.0.2.2 for localhost.
    
    base_url = request.host_url.rstrip('/')
    stream_url = f"{base_url}/player?token={token}"
    
    return jsonify({
        "stream_url": stream_url
    })

@api_bp.route("/player", methods=["GET"])
def player():
    token = request.args.get("token")
    if not token:
        return "Unauthorized", 401
    
    try:
        payload = jwt.decode(token, VIDEO_PLAYBACK_SECRET, algorithms=["HS256"])
        youtube_id = payload["video_id"]
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return "Invalid Token", 403

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body, html {{ margin: 0; padding: 0; height: 100%; overflow: hidden; background: #000; }}
            iframe {{ width: 100%; height: 100%; border: 0; }}
        </style>
    </head>
    <body>
        <iframe 
            src="https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1" 
            allowfullscreen 
            allow="autoplay; encrypted-media">
        </iframe>
    </body>
    </html>
    """
    return render_template_string(html)
