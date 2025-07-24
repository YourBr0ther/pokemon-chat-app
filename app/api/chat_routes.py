from flask import Blueprint, jsonify, request
from app.models.pokemon import db, Pokemon, ChatMessage, TeamMember
from app.personality.chat_engine import ChatEngine

chat_bp = Blueprint('chat', __name__)
chat_engine = ChatEngine()

@chat_bp.route('/pokemon/<int:pokemon_id>/messages', methods=['GET'])
def get_chat_history(pokemon_id):
    """Get chat history for a Pokemon"""
    try:
        pokemon = Pokemon.query.get_or_404(pokemon_id)
        messages = ChatMessage.query.filter_by(pokemon_id=pokemon_id).order_by(ChatMessage.timestamp).all()
        
        return jsonify({
            'success': True,
            'pokemon': pokemon.to_dict(),
            'messages': [msg.to_dict() for msg in messages]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/pokemon/<int:pokemon_id>/send', methods=['POST'])
def send_message(pokemon_id):
    """Send message to Pokemon and get response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        pokemon = Pokemon.query.get_or_404(pokemon_id)
        
        # Save user message
        user_chat = ChatMessage(
            pokemon_id=pokemon_id,
            message=user_message,
            sender='user'
        )
        db.session.add(user_chat)
        
        # Get recent conversation history for context
        recent_messages = ChatMessage.query.filter_by(pokemon_id=pokemon_id)\
            .order_by(ChatMessage.timestamp.desc())\
            .limit(10).all()
        
        conversation_history = [
            {'sender': msg.sender, 'message': msg.message}
            for msg in reversed(recent_messages)
        ]
        
        # Generate Pokemon response
        pokemon_data = pokemon.to_dict()
        response = chat_engine.generate_response(
            pokemon_data, 
            user_message, 
            conversation_history
        )
        
        # Save Pokemon response
        pokemon_chat = ChatMessage(
            pokemon_id=pokemon_id,
            message=response,
            sender='pokemon'
        )
        db.session.add(pokemon_chat)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user_message': user_chat.to_dict(),
            'pokemon_response': pokemon_chat.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/team/active', methods=['GET'])
def get_active_team():
    """Get active team for chat sidebar"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        team_members = TeamMember.query.filter_by(user_id=user_id)\
            .order_by(TeamMember.slot_number).all()
        
        return jsonify({
            'success': True,
            'team': [tm.to_dict() for tm in team_members]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/pokemon/<int:pokemon_id>/clear-history', methods=['POST'])
def clear_chat_history(pokemon_id):
    """Clear chat history for a Pokemon"""
    try:
        pokemon = Pokemon.query.get_or_404(pokemon_id)
        
        # Delete all messages for this Pokemon
        ChatMessage.query.filter_by(pokemon_id=pokemon_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Chat history with {pokemon.nickname} has been cleared'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500