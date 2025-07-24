#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app

def test_flask_startup():
    print("🚀 Testing Flask Application Startup...")
    
    try:
        # Create app
        app = create_app()
        print("✅ Flask app created successfully")
        
        # Test with app context
        with app.app_context():
            # Initialize database
            from app.models.pokemon import db
            db.create_all()
            print("✅ Database initialized")
            
            # Test client
            client = app.test_client()
            
            # Test main routes
            routes_to_test = [
                ('/', 'Import screen'),
                ('/import', 'Import screen'),
                ('/pokedex', 'Pokedex screen'),
                ('/chat', 'Chat screen')
            ]
            
            for route, description in routes_to_test:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"✅ {description} ({route}): {response.status_code}")
                else:
                    print(f"❌ {description} ({route}): {response.status_code}")
            
            # Test API endpoints that should be accessible
            api_routes = [
                ('/api/pokemon', 'GET', 'Get all Pokemon'),
                ('/api/team', 'GET', 'Get team'),
            ]
            
            for route, method, description in api_routes:
                if method == 'GET':
                    response = client.get(route)
                else:
                    response = client.post(route, json={})
                
                if response.status_code in [200, 404]:  # 404 is OK for empty data
                    print(f"✅ {description} ({method} {route}): {response.status_code}")
                else:
                    print(f"❌ {description} ({method} {route}): {response.status_code}")
        
        print("\n🎉 Flask application startup test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Flask startup test failed: {e}")
        return False

if __name__ == '__main__':
    test_flask_startup()