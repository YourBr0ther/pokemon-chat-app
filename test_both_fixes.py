#!/usr/bin/env python3

import sys
import os
import io
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app

def test_both_fixes():
    print("🧪 Testing Both Fixes: File Size + Double Import...")
    
    app = create_app()
    
    with app.app_context():
        # Initialize fresh database
        from app.models.pokemon import db
        db.drop_all()
        db.create_all()
        
        client = app.test_client()
        
        # Test 1: File size flexibility
        print("\n📏 Testing File Size Flexibility...")
        
        with open('test_celebi.pk8', 'rb') as f:
            original_data = f.read()
        
        # Test slightly different sizes
        test_sizes = [320, 344, 368]
        
        for size in test_sizes:
            print(f"   Testing {size} bytes...")
            
            if size < len(original_data):
                test_data = original_data[:size]
            else:
                test_data = original_data + b'\x00' * (size - len(original_data))
            
            response = client.post('/api/upload', 
                                 data={'file': (io.BytesIO(test_data), f'test_{size}.pk8')},
                                 content_type='multipart/form-data')
            
            if response.status_code == 200:
                data = response.get_json()
                level = data['pokemon_data']['level']
                print(f"      ✅ {size} bytes: Parsed successfully (Level: {level})")
            else:
                print(f"      ❌ {size} bytes: Failed - {response.status_code}")
        
        # Test 2: Double import prevention
        print(f"\n🔄 Testing Double Import Prevention...")
        
        # First import
        response1 = client.post('/api/upload', 
                               data={'file': (io.BytesIO(original_data), 'celebi.pk8')},
                               content_type='multipart/form-data')
        
        if response1.status_code == 200:
            upload_data = response1.get_json()
            
            # Save first time
            save_data = {
                'pokemon_data': upload_data['pokemon_data'],
                'personality_traits': upload_data['personality_traits']
            }
            
            response2 = client.post('/api/save',
                                   data=json.dumps(save_data),
                                   content_type='application/json')
            
            if response2.status_code == 200:
                print("      ✅ First import successful")
                
                # Try to save the same Pokemon again
                response3 = client.post('/api/save',
                                       data=json.dumps(save_data),
                                       content_type='application/json')
                
                if response3.status_code == 409:  # Conflict
                    error_data = response3.get_json()
                    print(f"      ✅ Duplicate prevented: {error_data['error']}")
                else:
                    print(f"      ❌ Duplicate not prevented: {response3.status_code}")
            else:
                print(f"      ❌ First save failed: {response2.status_code}")
        else:
            print(f"      ❌ Upload failed: {response1.status_code}")
        
        # Test 3: Import different Pokemon with same species
        print(f"\n🔄 Testing Different Pokemon Same Species...")
        
        # Modify the level to create a "different" Celebi
        modified_data = upload_data['pokemon_data'].copy()
        modified_data['level'] = 50  # Different level
        
        save_data_modified = {
            'pokemon_data': modified_data,
            'personality_traits': upload_data['personality_traits']
        }
        
        response4 = client.post('/api/save',
                               data=json.dumps(save_data_modified),
                               content_type='application/json')
        
        if response4.status_code == 200:
            print("      ✅ Different Celebi (Level 50) imported successfully")
        else:
            error_data = response4.get_json()
            print(f"      ❌ Different Celebi rejected: {error_data.get('error', 'Unknown error')}")
        
        print(f"\n🎉 All tests completed!")

if __name__ == '__main__':
    test_both_fixes()