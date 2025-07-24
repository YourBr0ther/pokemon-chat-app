#!/usr/bin/env python3
"""
Test script to verify the double import fix is working
"""

import sys
import os
import io
import json
import time
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app

def test_double_import_prevention():
    """Test that the same Pokemon cannot be imported twice"""
    print("🧪 Testing Double Import Prevention...")
    
    app = create_app()
    
    with app.app_context():
        # Initialize fresh database
        from app.models.pokemon import db
        db.drop_all()
        db.create_all()
        
        client = app.test_client()
        
        # Simulate a Pokemon import
        test_pokemon_data = {
            'species_id': 810,
            'species_name': 'Grookey',
            'nickname': 'Grookey',
            'level': 100,
            'nature': 'Hasty',
            'friendship': 50,
            'trainer_name': 'TestTrainer',
            'types': ['Grass'],
            'ivs': {
                'hp': 31,
                'attack': 31,
                'defense': 31,
                'sp_attack': 31,
                'sp_defense': 31,
                'speed': 31
            },
            'encryption_key': 12345,
            # PokeAPI data
            'sprite_url': 'https://example.com/grookey.png',
            'genus': 'Chimp Pokémon',
            'description': 'Test description',
            'height': 3,
            'weight': 50,
            'is_legendary': False,
            'is_mythical': False
        }
        
        test_personality = {
            'species_personality': 'energetic',
            'type_influence': 'natural',
            'nature_traits': 'hasty',
            'friendship_level': 'warming_up',
            'level_maturity': 'wise'
        }
        
        save_data = {
            'pokemon_data': test_pokemon_data,
            'personality_traits': test_personality
        }
        
        # First import - should succeed
        print("   Testing first import...")
        response1 = client.post('/api/save',
                               data=json.dumps(save_data),
                               content_type='application/json')
        
        if response1.status_code == 200:
            result1 = response1.get_json()
            print(f"   ✅ First import successful: {result1['message']}")
        else:
            print(f"   ❌ First import failed: {response1.status_code}")
            return False
        
        # Second import - should be prevented
        print("   Testing second import (should be prevented)...")
        response2 = client.post('/api/save',
                               data=json.dumps(save_data),
                               content_type='application/json')
        
        if response2.status_code == 409:  # Conflict status code
            result2 = response2.get_json()
            print(f"   ✅ Second import correctly prevented: {result2['error']}")
        else:
            print(f"   ❌ Second import not prevented: {response2.status_code}")
            return False
        
        # Test with different IVs - should be allowed
        print("   Testing similar Pokemon with different IVs...")
        test_pokemon_data_different = test_pokemon_data.copy()
        test_pokemon_data_different['ivs'] = {
            'hp': 30,  # Different IV
            'attack': 30,
            'defense': 30,
            'sp_attack': 30,
            'sp_defense': 30,
            'speed': 30
        }
        
        save_data_different = {
            'pokemon_data': test_pokemon_data_different,
            'personality_traits': test_personality
        }
        
        response3 = client.post('/api/save',
                               data=json.dumps(save_data_different),
                               content_type='application/json')
        
        if response3.status_code == 200:
            result3 = response3.get_json()
            print(f"   ✅ Different IV Pokemon allowed: {result3['message']}")
        else:
            print(f"   ❌ Different IV Pokemon blocked: {response3.status_code}")
            return False
        
        return True

def main():
    """Run the double import test"""
    print("🚀 Testing Double Import Fix...\n")
    
    if test_double_import_prevention():
        print("\n🎉 All tests passed! Double import issue is fixed!")
        return True
    else:
        print("\n❌ Tests failed! Double import issue persists.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)