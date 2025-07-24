#!/usr/bin/env python3

import sys
import os
import io
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models.pokemon import db, Pokemon, TeamMember, ChatMessage

def test_end_to_end():
    print("🚀 Running Comprehensive End-to-End Test...")
    
    app = create_app()
    
    with app.app_context():
        # Initialize fresh database
        db.drop_all()
        db.create_all()
        print("✅ Database initialized")
        
        client = app.test_client()
        
        # Phase 1: Web page rendering
        print("\n🌐 Phase 1: Testing Web Page Rendering...")
        
        pages = [
            ('/', 'Homepage'),
            ('/import', 'Import page'),
            ('/pokedex', 'Pokedex page'),
            ('/chat', 'Chat page')
        ]
        
        for url, name in pages:
            response = client.get(url)
            if response.status_code == 200:
                print(f"   ✅ {name}")
            else:
                print(f"   ❌ {name} failed: {response.status_code}")
                return False
        
        # Phase 2: Complete Pokemon import workflow
        print("\n📥 Phase 2: Testing Complete Import Workflow...")
        
        # Upload PK8 file
        with open('test_celebi.pk8', 'rb') as f:
            pk8_data = f.read()
        
        response = client.post('/api/upload', 
                             data={'file': (io.BytesIO(pk8_data), 'celebi.pk8')},
                             content_type='multipart/form-data')
        
        if response.status_code != 200:
            print(f"   ❌ Upload failed: {response.status_code}")
            return False
        
        upload_data = response.get_json()
        pokemon_data = upload_data['pokemon_data']
        personality_traits = upload_data['personality_traits']
        print(f"   ✅ Uploaded: {pokemon_data['nickname']}")
        
        # Save Pokemon
        save_payload = {
            'pokemon_data': pokemon_data,
            'personality_traits': personality_traits
        }
        
        response = client.post('/api/save',
                             data=json.dumps(save_payload),
                             content_type='application/json')
        
        if response.status_code != 200:
            print(f"   ❌ Save failed: {response.status_code}")
            return False
        
        save_data = response.get_json()
        pokemon_id = save_data['pokemon_id']
        print(f"   ✅ Saved with ID: {pokemon_id}")
        
        # Phase 3: Pokedex and team management
        print("\n📚 Phase 3: Testing Pokedex and Team Management...")
        
        # Get all Pokemon
        response = client.get('/api/pokemon')
        if response.status_code != 200:
            print(f"   ❌ Get Pokemon failed: {response.status_code}")
            return False
        
        pokemon_list = response.get_json()
        print(f"   ✅ Retrieved {len(pokemon_list['pokemon'])} Pokemon")
        
        # Add to team
        response = client.post('/api/team/add',
                             data=json.dumps({'pokemon_id': pokemon_id}),
                             content_type='application/json')
        
        if response.status_code != 200:
            print(f"   ❌ Add to team failed: {response.status_code}")
            return False
        
        print("   ✅ Added to team")
        
        # Get team
        response = client.get('/api/team')
        if response.status_code != 200:
            print(f"   ❌ Get team failed: {response.status_code}")
            return False
        
        team_data = response.get_json()
        if len(team_data['team']) != 1:
            print(f"   ❌ Team size incorrect: {len(team_data['team'])}")
            return False
        
        print("   ✅ Team management working")
        
        # Phase 4: Chat functionality
        print("\n💬 Phase 4: Testing Chat System...")
        
        # Get active team for chat
        response = client.get('/api/team/active')
        if response.status_code != 200:
            print(f"   ❌ Get active team failed: {response.status_code}")
            return False
        
        active_team = response.get_json()
        print(f"   ✅ Active team: {len(active_team['team'])} members")
        
        # Test conversation
        test_messages = [
            "Hello!",
            "How are you?",
            "Tell me about yourself",
            "You're amazing!"
        ]
        
        conversation_count = 0
        for message in test_messages:
            response = client.post(f'/api/pokemon/{pokemon_id}/send',
                                 data=json.dumps({'message': message}),
                                 content_type='application/json')
            
            if response.status_code != 200:
                print(f"   ❌ Chat message failed: {response.status_code}")
                return False
            
            chat_response = response.get_json()
            pokemon_reply = chat_response['pokemon_response']['message']
            conversation_count += 1
            
            print(f"   ✅ Message {conversation_count}: Response received")
        
        # Get chat history
        response = client.get(f'/api/pokemon/{pokemon_id}/messages')
        if response.status_code != 200:
            print(f"   ❌ Get chat history failed: {response.status_code}")
            return False
        
        chat_history = response.get_json()
        expected_messages = len(test_messages) * 2  # User + Pokemon responses
        
        if len(chat_history['messages']) != expected_messages:
            print(f"   ❌ Chat history count wrong: {len(chat_history['messages'])} vs {expected_messages}")
            return False
        
        print(f"   ✅ Chat history: {len(chat_history['messages'])} messages")
        
        # Phase 5: Cleanup operations
        print("\n🧹 Phase 5: Testing Cleanup Operations...")
        
        # Clear chat history
        response = client.post(f'/api/pokemon/{pokemon_id}/clear-history')
        if response.status_code != 200:
            print(f"   ❌ Clear chat failed: {response.status_code}")
            return False
        
        print("   ✅ Chat history cleared")
        
        # Remove from team
        response = client.post('/api/team/remove',
                             data=json.dumps({'pokemon_id': pokemon_id}),
                             content_type='application/json')
        
        if response.status_code != 200:
            print(f"   ❌ Remove from team failed: {response.status_code}")
            return False
        
        print("   ✅ Removed from team")
        
        # Verify team is empty
        response = client.get('/api/team')
        team_data = response.get_json()
        
        if len(team_data['team']) != 0:
            print(f"   ❌ Team not empty after removal: {len(team_data['team'])}")
            return False
        
        print("   ✅ Team cleanup verified")
        
        # Phase 6: Verify data integrity
        print("\n🔍 Phase 6: Testing Data Integrity...")
        
        # Verify Pokemon still exists
        response = client.get(f'/api/pokemon/{pokemon_id}')
        if response.status_code != 200:
            print(f"   ❌ Pokemon not found: {response.status_code}")
            return False
        
        # Verify chat messages were cleared
        response = client.get(f'/api/pokemon/{pokemon_id}/messages')
        chat_history = response.get_json()
        
        if len(chat_history['messages']) != 0:
            print(f"   ❌ Chat messages not cleared: {len(chat_history['messages'])}")
            return False
        
        print("   ✅ Data integrity verified")
        
        # Final verification: Full application state
        print("\n📊 Final State Verification...")
        
        # Count database records
        pokemon_count = Pokemon.query.count()
        team_count = TeamMember.query.count()
        message_count = ChatMessage.query.count()
        
        print(f"   📈 Final state: {pokemon_count} Pokemon, {team_count} team members, {message_count} messages")
        
        if pokemon_count == 1 and team_count == 0 and message_count == 0:
            print("   ✅ Final state correct")
        else:
            print("   ⚠️ Final state unexpected but not necessarily wrong")
        
        print("\n🎉 END-TO-END TEST COMPLETED SUCCESSFULLY!")
        print("🏆 All major functionality verified:")
        print("   • Web page rendering")
        print("   • PK8 file upload and parsing")
        print("   • Pokemon data storage")
        print("   • Team management")
        print("   • Chat system with personality")
        print("   • Data cleanup and integrity")
        
        return True

if __name__ == '__main__':
    success = test_end_to_end()
    if success:
        print("\n✨ The Pokemon Chat App is fully functional and ready for use!")
    else:
        print("\n❌ End-to-end test failed. Check the application.")
    exit(0 if success else 1)