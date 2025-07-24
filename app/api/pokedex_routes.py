from flask import Blueprint, jsonify, request
from app.models.pokemon import db, Pokemon, TeamMember

pokedex_bp = Blueprint('pokedex', __name__)

@pokedex_bp.route('/pokemon', methods=['GET'])
def get_all_pokemon():
    """Get all Pokemon in Pokedex"""
    try:
        pokemon_list = Pokemon.query.order_by(Pokemon.created_at.desc()).all()
        return jsonify({
            'success': True,
            'pokemon': [p.to_dict() for p in pokemon_list]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokedex_bp.route('/pokemon/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    """Get specific Pokemon by ID"""
    try:
        pokemon = Pokemon.query.get_or_404(pokemon_id)
        return jsonify({
            'success': True,
            'pokemon': pokemon.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokedex_bp.route('/team', methods=['GET'])
def get_team():
    """Get current team composition"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        team_members = TeamMember.query.filter_by(user_id=user_id).order_by(TeamMember.slot_number).all()
        
        return jsonify({
            'success': True,
            'team': [tm.to_dict() for tm in team_members]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokedex_bp.route('/team/add', methods=['POST'])
def add_to_team():
    """Add Pokemon to team"""
    try:
        data = request.get_json()
        pokemon_id = data.get('pokemon_id')
        user_id = data.get('user_id', 'default_user')
        
        if not pokemon_id:
            return jsonify({'error': 'Pokemon ID is required'}), 400
        
        # Check if Pokemon exists
        pokemon = Pokemon.query.get_or_404(pokemon_id)
        
        # Check if Pokemon is already on team
        existing = TeamMember.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
        if existing:
            return jsonify({'error': f'{pokemon.nickname} is already on your team'}), 400
        
        # Check team size (max 6)
        team_size = TeamMember.query.filter_by(user_id=user_id).count()
        if team_size >= 6:
            return jsonify({'error': 'Team is full! Remove a Pokemon first.'}), 400
        
        # Find next available slot
        used_slots = [tm.slot_number for tm in TeamMember.query.filter_by(user_id=user_id).all()]
        slot_number = 1
        while slot_number in used_slots and slot_number <= 6:
            slot_number += 1
        
        # Add to team
        team_member = TeamMember(
            user_id=user_id,
            pokemon_id=pokemon_id,
            slot_number=slot_number
        )
        
        db.session.add(team_member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{pokemon.nickname} joined your team!',
            'team_member': team_member.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pokedex_bp.route('/team/remove', methods=['POST'])
def remove_from_team():
    """Remove Pokemon from team"""
    try:
        data = request.get_json()
        pokemon_id = data.get('pokemon_id')
        user_id = data.get('user_id', 'default_user')
        
        if not pokemon_id:
            return jsonify({'error': 'Pokemon ID is required'}), 400
        
        # Find team member
        team_member = TeamMember.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
        if not team_member:
            return jsonify({'error': 'Pokemon is not on your team'}), 404
        
        pokemon_nickname = team_member.pokemon.nickname
        
        # Remove from team
        db.session.delete(team_member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{pokemon_nickname} was removed from your team'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pokedex_bp.route('/pokemon/<int:pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    """Delete Pokemon from Pokedex"""
    try:
        pokemon = Pokemon.query.get_or_404(pokemon_id)
        pokemon_nickname = pokemon.nickname
        
        # This will cascade delete team members and chat messages
        db.session.delete(pokemon)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{pokemon_nickname} was released from your Pokedex'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500