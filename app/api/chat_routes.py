from flask import Blueprint, jsonify, request, current_app
from flask_wtf.csrf import validate_csrf
from app.models.pokemon import db, Pokemon, ChatMessage, TeamMember
from app.personality.chat_engine import ChatEngine
from app.schemas import ChatMessageSchema, validate_json_input, sanitize_html_content
from app.extensions import limiter

chat_bp = Blueprint('chat', __name__)
chat_engine = ChatEngine()

@chat_bp.route('/pokemon/<int:pokemon_id>/messages', methods=['GET'])
@limiter.limit("30 per minute")  # Allow frequent message checking
def get_chat_history(pokemon_id):
    """Get chat history for a Pokemon"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        pokemon = Pokemon.query.get_or_404(pokemon_id)
        logger.info(f"Loading chat history for Pokemon ID {pokemon_id}: {pokemon.nickname}")
        
        messages = ChatMessage.query.filter_by(pokemon_id=pokemon_id).order_by(ChatMessage.timestamp).all()
        logger.info(f"Found {len(messages)} messages for {pokemon.nickname}")
        
        # Convert pokemon to dict with error handling
        pokemon_dict = pokemon.to_dict()
        logger.info(f"Successfully converted Pokemon {pokemon.nickname} to dict")
        
        return jsonify({
            'success': True,
            'pokemon': pokemon_dict,
            'messages': [msg.to_dict() for msg in messages]
        })
        
    except Exception as e:
        logger.error(f"Error loading chat history for Pokemon ID {pokemon_id}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Failed to load Pokemon chat: {str(e)}'}), 500

@chat_bp.route('/pokemon/<int:pokemon_id>/send', methods=['POST'])
@limiter.limit("20 per minute")  # Prevent chat spam while allowing normal conversation
def send_message(pokemon_id):
    """Send message to Pokemon and get response with validation"""
    try:
        # Validate CSRF token
        try:
            validate_csrf(request.headers.get('X-CSRFToken'))
        except Exception as e:
            current_app.logger.warning(f"CSRF validation failed: {str(e)}")
            return jsonify({'error': 'CSRF token missing or invalid'}), 403
            
        data = request.get_json()
        
        # Validate input using schema
        is_valid, validated_data = validate_json_input(ChatMessageSchema, data)
        if not is_valid:
            return jsonify({'error': 'Invalid message data', 'details': validated_data}), 400
        
        user_message = validated_data['message'].strip()
        # Additional sanitization
        user_message = sanitize_html_content(user_message)
        
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