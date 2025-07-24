from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Redirect to import screen by default"""
    return render_template('import.html')

@main_bp.route('/import')
def import_screen():
    """Import screen for uploading PK8 files"""
    return render_template('import.html')

@main_bp.route('/pokedex')
def pokedex_screen():
    """Pokedex screen for viewing and managing Pokemon"""
    return render_template('pokedex.html')

@main_bp.route('/chat')
def chat_screen():
    """Chat screen for talking with Pokemon"""
    return render_template('chat.html')