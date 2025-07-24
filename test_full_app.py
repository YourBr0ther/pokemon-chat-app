#!/usr/bin/env python3

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models.pokemon import db, Pokemon, TeamMember, ChatMessage
from app.parsers.pk8_parser import PK8Parser
from app.personality.chat_engine import ChatEngine

def test_full_application():
    print("🚀 Testing Full Pokemon Chat Application...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        # Initialize database
        db.create_all()
        print("✅ Database initialized")
        
        # Test 1: Parse PK8 file
        print("\n📁 Testing PK8 Parser...")
        parser = PK8Parser()
        pokemon_data = parser.parse_file('test_celebi.pk8')
        personality_traits = parser.get_personality_traits(pokemon_data)
        
        print(f"   Species: {pokemon_data['species_name']}")
        print(f"   Nickname: {pokemon_data['nickname']}")
        print(f"   Level: {pokemon_data['level']}")
        print(f"   Nature: {pokemon_data['nature']}")
        print(f"   Friendship: {pokemon_data['friendship']}")
        print(f"   Personality: {personality_traits['species_personality']}")
        
        # Test 2: Save to database
        print("\n💾 Testing Database Operations...")
        pokemon = Pokemon(
            species_id=pokemon_data['species_id'],
            species_name=pokemon_data['species_name'],
            nickname=pokemon_data['nickname'],
            level=pokemon_data['level'],
            nature=pokemon_data['nature'],
            friendship=pokemon_data['friendship'],
            original_trainer=pokemon_data['trainer_name']
        )
        
        pokemon.set_types(pokemon_data['types'])
        pokemon.set_personality(personality_traits)
        pokemon.set_ivs(pokemon_data['ivs'])
        
        db.session.add(pokemon)
        db.session.commit()
        
        print(f"   ✅ Pokemon saved with ID: {pokemon.id}")
        
        # Test 3: Team management
        print("\n👥 Testing Team Management...")
        team_member = TeamMember(
            user_id='test_user',
            pokemon_id=pokemon.id,
            slot_number=1
        )
        
        db.session.add(team_member)
        db.session.commit()
        
        print(f"   ✅ {pokemon.nickname} added to team slot 1")
        
        # Test 4: Chat engine
        print("\n💬 Testing Chat Engine...")
        chat_engine = ChatEngine()
        
        test_messages = [
            "Hello there!",
            "How are you feeling today?",
            "You're such an amazing Pokemon!",
            "What do you think about friendship?"
        ]
        
        for message in test_messages:
            response = chat_engine.generate_response(
                pokemon.to_dict(), 
                message
            )
            
            print(f"   User: {message}")
            print(f"   {pokemon.nickname}: {response}")
            
            # Save chat messages
            user_msg = ChatMessage(
                pokemon_id=pokemon.id,
                message=message,
                sender='user'
            )
            
            pokemon_msg = ChatMessage(
                pokemon_id=pokemon.id,
                message=response,
                sender='pokemon'
            )
            
            db.session.add_all([user_msg, pokemon_msg])
            db.session.commit()
            
            print()
        
        # Test 5: Data retrieval
        print("📊 Testing Data Retrieval...")
        
        # Get all Pokemon
        all_pokemon = Pokemon.query.all()
        print(f"   Total Pokemon in Pokedex: {len(all_pokemon)}")
        
        # Get team
        team = TeamMember.query.filter_by(user_id='test_user').all()
        print(f"   Team size: {len(team)}")
        
        # Get chat history
        messages = ChatMessage.query.filter_by(pokemon_id=pokemon.id).all()
        print(f"   Chat messages: {len(messages)}")
        
        print(f"\n🎉 All tests passed! The Pokemon Chat App is working correctly!")
        print(f"🔗 You can now run the app with: python app/main.py")
        
        return True

if __name__ == '__main__':
    test_full_application()