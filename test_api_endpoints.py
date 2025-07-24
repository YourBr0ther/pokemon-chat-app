#!/usr/bin/env python3

import sys
import os
import io
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models.pokemon import db, Pokemon, TeamMember, ChatMessage

def test_api_endpoints():
    print("🌐 Testing API Endpoints...")
    
    app = create_app()
    
    with app.app_context():
        # Initialize database
        db.drop_all()
        db.create_all()
        
        client = app.test_client()
        
        # Test 1: Upload PK8 file
        print("\n📤 Testing PK8 Upload...")
        
        with open('test_celebi.pk8', 'rb') as f:
            pk8_data = f.read()
        
        response = client.post('/api/upload', 
                             data={'file': (io.BytesIO(pk8_data), 'celebi.pk8')},
                             content_type='multipart/form-data')
        
        if response.status_code == 200:
            print("   ✅ PK8 upload successful")
            upload_data = response.get_json()
            pokemon_data = upload_data['pokemon_data']
            personality_traits = upload_data['personality_traits']
            print(f"   ✅ Parsed: {pokemon_data['nickname']} ({pokemon_data['species_name']})")
        else:
            print(f"   ❌ PK8 upload failed: {response.status_code}")
            return False
        
        # Test 2: Save Pokemon
        print("\n💾 Testing Pokemon Save...")
        
        save_data = {
            'pokemon_data': pokemon_data,
            'personality_traits': personality_traits
        }
        
        response = client.post('/api/save',
                             data=json.dumps(save_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("   ✅ Pokemon save successful")
            save_response = response.get_json()
            pokemon_id = save_response['pokemon_id']
            print(f"   ✅ Pokemon ID: {pokemon_id}")
        else:
            print(f"   ❌ Pokemon save failed: {response.status_code}")
            return False
        
        # Test 3: Get all Pokemon
        print("\n📋 Testing Get All Pokemon...")
        
        response = client.get('/api/pokemon')
        
        if response.status_code == 200:
            pokemon_list = response.get_json()
            print(f"   ✅ Retrieved {len(pokemon_list['pokemon'])} Pokemon")
        else:
            print(f"   ❌ Get Pokemon failed: {response.status_code}")
            return False
        
        # Test 4: Get specific Pokemon
        print("\n🔍 Testing Get Specific Pokemon...")
        
        response = client.get(f'/api/pokemon/{pokemon_id}')
        
        if response.status_code == 200:
            pokemon_detail = response.get_json()
            print(f"   ✅ Retrieved Pokemon: {pokemon_detail['pokemon']['nickname']}")
        else:
            print(f"   ❌ Get specific Pokemon failed: {response.status_code}")
            return False
        
        # Test 5: Add to Team
        print("\n👥 Testing Add to Team...")
        
        team_data = {'pokemon_id': pokemon_id}
        response = client.post('/api/team/add',
                             data=json.dumps(team_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("   ✅ Added to team successfully")
        else:
            print(f"   ❌ Add to team failed: {response.status_code}")
            return False
        
        # Test 6: Get Team
        print("\n📊 Testing Get Team...")
        
        response = client.get('/api/team')
        
        if response.status_code == 200:
            team_data = response.get_json()
            print(f"   ✅ Team has {len(team_data['team'])} members")
        else:
            print(f"   ❌ Get team failed: {response.status_code}")
            return False
        
        # Test 7: Send Chat Message
        print("\n💬 Testing Chat Message...")
        
        chat_data = {'message': 'Hello there!'}
        response = client.post(f'/api/pokemon/{pokemon_id}/send',
                             data=json.dumps(chat_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            chat_response = response.get_json()
            print("   ✅ Chat message sent successfully")
            print(f"   ✅ Response: {chat_response['pokemon_response']['message'][:50]}...")
        else:
            print(f"   ❌ Chat message failed: {response.status_code}")
            return False
        
        # Test 8: Get Chat History
        print("\n📜 Testing Get Chat History...")
        
        response = client.get(f'/api/pokemon/{pokemon_id}/messages')
        
        if response.status_code == 200:
            chat_history = response.get_json()
            print(f"   ✅ Retrieved {len(chat_history['messages'])} messages")
        else:
            print(f"   ❌ Get chat history failed: {response.status_code}")
            return False
        
        # Test 9: Get Active Team (for chat)
        print("\n🎯 Testing Get Active Team...")
        
        response = client.get('/api/team/active')
        
        if response.status_code == 200:
            active_team = response.get_json()
            print(f"   ✅ Active team has {len(active_team['team'])} members")
        else:
            print(f"   ❌ Get active team failed: {response.status_code}")
            return False
        
        # Test 10: Remove from Team
        print("\n➖ Testing Remove from Team...")
        
        remove_data = {'pokemon_id': pokemon_id}
        response = client.post('/api/team/remove',
                             data=json.dumps(remove_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("   ✅ Removed from team successfully")
        else:
            print(f"   ❌ Remove from team failed: {response.status_code}")
            return False
        
        # Test 11: Clear Chat History
        print("\n🧹 Testing Clear Chat History...")
        
        response = client.post(f'/api/pokemon/{pokemon_id}/clear-history')
        
        if response.status_code == 200:
            print("   ✅ Chat history cleared successfully")
        else:
            print(f"   ❌ Clear chat history failed: {response.status_code}")
            return False
        
        print("\n🎉 All API endpoint tests passed!")
        return True

if __name__ == '__main__':
    test_api_endpoints()