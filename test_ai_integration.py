#!/usr/bin/env python3
"""
Test script to verify AI-powered Pokemon chat integration
"""

import sys
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_ai_service():
    """Test the AI service directly"""
    print("🧪 Testing AI Chat Service...")
    
    try:
        from app.services.ai_chat_service import AIChatService
        
        service = AIChatService()
        print(f"   AI Service available: {service.is_available()}")
        
        if service.is_available():
            print(f"   Available providers: {[p.value for p in service.available_providers]}")
            print(f"   Preferred provider: {service.preferred_provider}")
            
            # Test with sample Pokemon data
            test_pokemon = {
                'species_id': 25,
                'species_name': 'Pikachu',
                'nickname': 'Sparky',
                'level': 45,
                'nature': 'Jolly',
                'friendship': 150,
                'types': ['Electric'],
                'genus': 'Mouse Pokémon',
                'description': 'This Pokémon has electricity-storing pouches on its cheeks.',
                'personality': {
                    'species_personality': 'energetic',
                    'type_influence': 'energetic',
                    'nature_traits': 'upbeat',
                    'friendship_level': 'warming_up',
                    'level_maturity': 'mature'
                }
            }
            
            print("   Testing AI response generation...")
            response = service.generate_pokemon_response(
                "Hello Sparky! How are you feeling today?",
                test_pokemon
            )
            
            print(f"   ✅ AI Response: {response}")
            return True
        else:
            print("   ⚠️ No AI API keys configured")
            return False
            
    except Exception as e:
        print(f"   ❌ AI Service test failed: {e}")
        return False

def test_chat_engine():
    """Test the enhanced chat engine"""
    print("🧪 Testing Enhanced Chat Engine...")
    
    try:
        from app.personality.chat_engine import ChatEngine
        
        engine = ChatEngine()
        
        # Test with different Pokemon personalities
        test_cases = [
            {
                'pokemon': {
                    'species_id': 251,
                    'species_name': 'Celebi',
                    'nickname': 'Celebi',
                    'level': 63,
                    'nature': 'Modest',
                    'friendship': 4,  # Low friendship
                    'types': ['Psychic', 'Grass'],
                    'genus': 'Time Travel Pokémon',
                    'description': 'This Pokémon wanders across time.',
                    'is_mythical': True,
                    'personality': {
                        'species_personality': 'gentle',
                        'type_influence': 'thoughtful',
                        'nature_traits': 'humble',
                        'friendship_level': 'distant',
                        'level_maturity': 'wise'
                    }
                },
                'message': 'Hello there, what do you think about time travel?',
                'expected_tone': 'cautious and wise'
            },
            {
                'pokemon': {
                    'species_id': 810,
                    'species_name': 'Grookey',
                    'nickname': 'Grookey',
                    'level': 100,
                    'nature': 'Hasty',
                    'friendship': 200,  # High friendship
                    'types': ['Grass'],
                    'genus': 'Chimp Pokémon',
                    'description': 'When it uses its special stick to strike up a beat.',
                    'personality': {
                        'species_personality': 'energetic',
                        'type_influence': 'natural',
                        'nature_traits': 'hasty',
                        'friendship_level': 'loyal',
                        'level_maturity': 'wise'
                    }
                },
                'message': 'Want to play some music together?',
                'expected_tone': 'enthusiastic and loyal'
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            pokemon = test_case['pokemon']
            message = test_case['message']
            expected_tone = test_case['expected_tone']
            
            print(f"   Test {i}: {pokemon['nickname']} ({expected_tone})")
            print(f"      Friendship: {pokemon['friendship']}, Nature: {pokemon['nature']}")
            print(f"      Message: {message}")
            
            response = engine.generate_response(pokemon, message)
            print(f"      Response: {response}")
            print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Chat Engine test failed: {e}")
        return False

def test_full_integration():
    """Test the full Flask app integration"""
    print("🧪 Testing Full Flask App Integration...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.app_context():
            # Test that the app starts successfully
            print("   ✅ Flask app created successfully")
            
            # Check AI configuration
            ai_provider = app.config.get('AI_PROVIDER')
            openai_key = app.config.get('OPENAI_API_KEY')
            claude_key = app.config.get('CLAUDE_API_KEY')
            
            print(f"   AI Provider: {ai_provider}")
            print(f"   OpenAI configured: {'Yes' if openai_key else 'No'}")
            print(f"   Claude configured: {'Yes' if claude_key else 'No'}")
            
            # Test chat engine initialization
            from app.personality.chat_engine import ChatEngine
            engine = ChatEngine()
            print(f"   ✅ Chat engine initialized with AI: {engine.ai_service.is_available()}")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Full integration test failed: {e}")
        return False

def main():
    """Run all AI integration tests"""
    print("🚀 AI-Powered Pokemon Chat Integration Tests\n")
    
    # Check environment configuration
    print("🔧 Environment Configuration:")
    print(f"   AI_PROVIDER: {os.getenv('AI_PROVIDER', 'Not set')}")
    print(f"   OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    print(f"   CLAUDE_API_KEY: {'Set' if os.getenv('CLAUDE_API_KEY') else 'Not set'}")
    print()
    
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('CLAUDE_API_KEY'):
        print("⚠️  No AI API keys detected. Tests will verify fallback behavior.")
        print("💡 To test AI features, add API keys to .env file:")
        print("   OPENAI_API_KEY=your-openai-key")
        print("   CLAUDE_API_KEY=your-claude-key")
        print()
    
    tests = [
        ("AI Service", test_ai_service),
        ("Chat Engine", test_chat_engine),
        ("Full Integration", test_full_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✅ {test_name} test PASSED\n")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED\n")
        except Exception as e:
            print(f"💥 {test_name} test ERROR: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AI integration is working correctly!")
        if os.getenv('OPENAI_API_KEY') or os.getenv('CLAUDE_API_KEY'):
            print("🤖 AI-powered Pokemon chat is ready to use!")
        else:
            print("📝 Template-based chat is working (add AI keys for enhanced features).")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)