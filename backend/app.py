from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from extensions import mongo

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/videoapp")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "dev_jwt")

    mongo.init_app(app)

    # Import and register blueprints
    from auth import auth_bp
    from routes import api_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp, url_prefix="/")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
