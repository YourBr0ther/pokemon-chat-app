from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pokemon_chat.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Initialize extensions
    from app.models.pokemon import db
    db.init_app(app)
    
    # Register blueprints
    from app.api.import_routes import import_bp
    from app.api.chat_routes import chat_bp
    from app.api.pokedex_routes import pokedex_bp
    
    app.register_blueprint(import_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(pokedex_bp, url_prefix='/api')
    
    # Main routes
    from app.main_routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app