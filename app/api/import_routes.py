from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app.parsers.pk8_parser import PK8Parser
from app.models.pokemon import db, Pokemon

import_bp = Blueprint('import', __name__)

ALLOWED_EXTENSIONS = {'pk8'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@import_bp.route('/upload', methods=['POST'])
def upload_pk8_file():
    """Upload and parse PK8 file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .pk8 files are allowed'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse PK8 file
        parser = PK8Parser()
        pokemon_data = parser.parse_file(filepath)
        personality_traits = parser.get_personality_traits(pokemon_data)
        
        # Clean up temporary file
        os.remove(filepath)
        
        # Return parsed data for preview
        return jsonify({
            'success': True,
            'pokemon_data': pokemon_data,
            'personality_traits': personality_traits
        })
        
    except Exception as e:
        # Clean up file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({'error': str(e)}), 500

@import_bp.route('/save', methods=['POST'])
def save_pokemon():
    """Save parsed Pokemon data to database"""
    try:
        data = request.get_json()
        
        if not data or 'pokemon_data' not in data:
            return jsonify({'error': 'No Pokemon data provided'}), 400
        
        pokemon_data = data['pokemon_data']
        personality_traits = data.get('personality_traits', {})
        
        # Check if Pokemon already exists (based on species, nickname, level, nature, and trainer for uniqueness)
        potential_duplicates = Pokemon.query.filter_by(
            species_id=pokemon_data['species_id'],
            nickname=pokemon_data['nickname'],
            level=pokemon_data['level'],
            nature=pokemon_data['nature'],
            original_trainer=pokemon_data['trainer_name']
        ).all()
        
        # For exact duplicate detection, also check IVs
        if potential_duplicates:
            import json
            new_ivs = pokemon_data['ivs']
            for existing in potential_duplicates:
                try:
                    existing_ivs = json.loads(existing.ivs) if existing.ivs else {}
                    # Check if IVs match (indicating same pk8 file)
                    if (existing_ivs.get('hp') == new_ivs.get('hp') and
                        existing_ivs.get('attack') == new_ivs.get('attack') and
                        existing_ivs.get('defense') == new_ivs.get('defense') and
                        existing_ivs.get('sp_attack') == new_ivs.get('sp_attack') and
                        existing_ivs.get('sp_defense') == new_ivs.get('sp_defense') and
                        existing_ivs.get('speed') == new_ivs.get('speed')):
                        return jsonify({
                            'error': f'This exact {pokemon_data["nickname"]} (Level {pokemon_data["level"]}, {pokemon_data["nature"]}) is already in your Pokedex',
                            'existing_id': existing.id
                        }), 409  # Use 409 Conflict instead of 400
                except:
                    # If IV comparison fails, fall back to basic duplicate check
                    pass
            
            # If we get here, it's a similar Pokemon but with different IVs - allow it
            print(f"Allowing similar Pokemon with different IVs: {pokemon_data['nickname']}")
        
        # Create new Pokemon record
        pokemon = Pokemon(
            species_id=pokemon_data['species_id'],
            species_name=pokemon_data['species_name'],
            nickname=pokemon_data['nickname'],
            level=pokemon_data['level'],
            nature=pokemon_data['nature'],
            friendship=pokemon_data['friendship'],
            original_trainer=pokemon_data['trainer_name'],
            
            # PokeAPI enhanced data
            sprite_url=pokemon_data.get('sprite_url'),
            sprite_shiny_url=pokemon_data.get('sprite_shiny_url'),
            official_artwork_url=pokemon_data.get('official_artwork_url'),
            description=pokemon_data.get('description'),
            genus=pokemon_data.get('genus'),
            height=pokemon_data.get('height'),
            weight=pokemon_data.get('weight'),
            base_happiness=pokemon_data.get('base_happiness'),
            capture_rate=pokemon_data.get('capture_rate'),
            is_legendary=pokemon_data.get('is_legendary', False),
            is_mythical=pokemon_data.get('is_mythical', False),
            habitat=pokemon_data.get('habitat'),
            pokemon_color=pokemon_data.get('pokemon_color')
        )
        
        # Set complex fields
        pokemon.set_types(pokemon_data['types'])
        pokemon.set_personality(personality_traits)
        pokemon.set_ivs(pokemon_data['ivs'])
        
        # Set PokeAPI complex fields
        if pokemon_data.get('abilities'):
            pokemon.set_abilities(pokemon_data['abilities'])
        if pokemon_data.get('base_stats'):
            pokemon.set_base_stats(pokemon_data['base_stats'])
        
        # Save to database
        db.session.add(pokemon)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{pokemon.nickname} has been added to your Pokedex!',
            'pokemon_id': pokemon.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500