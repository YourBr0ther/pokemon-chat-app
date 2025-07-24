#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models.pokemon import db, Pokemon, TeamMember, ChatMessage

def test_database_models():
    print("🗄️ Testing Database Models and Relationships...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Initialize database
            db.drop_all()
            db.create_all()
            print("✅ Database tables created")
            
            # Test Pokemon model
            print("\n📝 Testing Pokemon Model...")
            pokemon = Pokemon(
                species_id=25,
                species_name="Pikachu",
                nickname="Sparky",
                level=50,
                nature="Jolly",
                friendship=200,
                original_trainer="Ash"
            )
            
            # Test complex field setters
            pokemon.set_types(["Electric"])
            pokemon.set_personality({"species_personality": "energetic"})
            pokemon.set_ivs({"hp": 31, "attack": 31, "defense": 31, "sp_attack": 31, "sp_defense": 31, "speed": 31})
            
            db.session.add(pokemon)
            db.session.commit()
            
            # Test getters
            types = pokemon.get_types()
            personality = pokemon.get_personality()
            ivs = pokemon.get_ivs()
            
            print(f"   ✅ Pokemon created: {pokemon.nickname} (ID: {pokemon.id})")
            print(f"   ✅ Types: {types}")
            print(f"   ✅ Personality: {personality}")
            print(f"   ✅ IVs: {ivs}")
            
            # Test to_dict method
            pokemon_dict = pokemon.to_dict()
            print(f"   ✅ to_dict() returns {len(pokemon_dict)} fields")
            
            # Test TeamMember model
            print("\n👥 Testing TeamMember Model...")
            team_member = TeamMember(
                user_id="test_user",
                pokemon_id=pokemon.id,
                slot_number=1
            )
            
            db.session.add(team_member)
            db.session.commit()
            
            print(f"   ✅ Team member created (ID: {team_member.id})")
            print(f"   ✅ Relationship test: {team_member.pokemon.nickname}")
            
            # Test ChatMessage model
            print("\n💬 Testing ChatMessage Model...")
            message1 = ChatMessage(
                pokemon_id=pokemon.id,
                message="Hello!",
                sender="user"
            )
            
            message2 = ChatMessage(
                pokemon_id=pokemon.id,
                message="Hi there!",
                sender="pokemon"
            )
            
            db.session.add_all([message1, message2])
            db.session.commit()
            
            print(f"   ✅ Chat messages created: {message1.id}, {message2.id}")
            
            # Test relationships
            print("\n🔗 Testing Model Relationships...")
            
            # Pokemon -> TeamMembers
            team_members = pokemon.team_members
            print(f"   ✅ Pokemon has {len(team_members)} team memberships")
            
            # Pokemon -> ChatMessages
            chat_messages = pokemon.chat_messages
            print(f"   ✅ Pokemon has {len(chat_messages)} chat messages")
            
            print("\n🎉 All database model tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False

if __name__ == '__main__':
    test_database_models()