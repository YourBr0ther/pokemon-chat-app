#!/usr/bin/env python3

import sys
import os
import io
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app

def test_corrected_import():
    print("🧪 Testing Corrected PK8 Import...")
    
    app = create_app()
    
    with app.app_context():
        client = app.test_client()
        
        # Test corrected import workflow
        with open('test_celebi.pk8', 'rb') as f:
            pk8_data = f.read()
        
        response = client.post('/api/upload', 
                             data={'file': (io.BytesIO(pk8_data), 'celebi.pk8')},
                             content_type='multipart/form-data')
        
        if response.status_code == 200:
            upload_data = response.get_json()
            pokemon_data = upload_data['pokemon_data']
            
            print("✅ Corrected values:")
            print(f"   Species: {pokemon_data['species_name']}")
            print(f"   Level: {pokemon_data['level']} (was 255)")
            print(f"   Nature: {pokemon_data['nature']}")
            print(f"   Friendship: {pokemon_data['friendship']}")
            print(f"   IVs: {pokemon_data['ivs']}")
            
            # Validate all values are now reasonable
            valid = True
            
            if not (1 <= pokemon_data['level'] <= 100):
                print(f"   ❌ Level {pokemon_data['level']} still invalid")
                valid = False
            
            for stat, value in pokemon_data['ivs'].items():
                if not (0 <= value <= 31):
                    print(f"   ❌ IV {stat}:{value} still invalid")
                    valid = False
            
            if valid:
                print("🎉 All values are now within realistic Pokemon ranges!")
                return True
            else:
                return False
        else:
            print(f"❌ Upload failed: {response.status_code}")
            return False

if __name__ == '__main__':
    test_corrected_import()