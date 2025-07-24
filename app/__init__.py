from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging

def create_app():
    # Load environment variables from .env file
    load_dotenv()
    
    app = Flask(__name__)
    
    # Configure logging
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pokemon_chat.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    
    # AI Configuration (stored in config for reference)
    app.config['AI_PROVIDER'] = os.environ.get('AI_PROVIDER', 'openai')
    app.config['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')
    app.config['CLAUDE_API_KEY'] = os.environ.get('CLAUDE_API_KEY')
    
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
    
    # Log AI configuration status
    ai_status = []
    if os.environ.get('OPENAI_API_KEY'):
        ai_status.append('OpenAI')
    if os.environ.get('CLAUDE_API_KEY'):
        ai_status.append('Claude')
    
    if ai_status:
        app.logger.info(f"🤖 AI Chat enabled with: {', '.join(ai_status)}")
        app.logger.info(f"🎯 Preferred AI provider: {app.config['AI_PROVIDER']}")
    else:
        app.logger.warning("⚠️  No AI API keys configured. Chat will use template responses.")
        app.logger.info("💡 Add OPENAI_API_KEY or CLAUDE_API_KEY to enable AI chat features")
    
    return app