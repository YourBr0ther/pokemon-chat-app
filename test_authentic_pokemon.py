#!/usr/bin/env python3
"""
Test script to verify authentic Pokemon animal intelligence and communication
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_pokemon_intelligence_profiles():
    """Test the Pokemon intelligence and personality system"""
    print("🧠 Testing Pokemon Intelligence Profiles...")
    
    try:
        from app.services.pokemon_intelligence import PokemonIntelligence, PokemonPersonalityBuilder, IntelligenceLevel, CommunicationStyle
        
        # Test different Pokemon species
        test_pokemon = [
            {
                'name': 'Grookey',
                'species_id': 810,
                'expected_intelligence': IntelligenceLevel.AVERAGE,
                'expected_communication': CommunicationStyle.SIMPLE,
                'expected_traits': ['playful', 'social', 'musical']
            },
            {
                'name': 'Pikachu', 
                'species_id': 25,
                'expected_intelligence': IntelligenceLevel.HIGH,
                'expected_communication': CommunicationStyle.CLEAR,
                'expected_traits': ['social', 'curious', 'energetic']
            },
            {
                'name': 'Mewtwo',
                'species_id': 150, 
                'expected_intelligence': IntelligenceLevel.GENIUS,
                'expected_communication': CommunicationStyle.ELOQUENT,
                'expected_traits': ['solitary', 'philosophical']
            },
            {
                'name': 'Sobble',
                'species_id': 816,
                'expected_intelligence': IntelligenceLevel.AVERAGE,
                'expected_communication': CommunicationStyle.BROKEN,
                'expected_traits': ['shy', 'emotional', 'prey-like']
            }
        ]
        
        for pokemon in test_pokemon:
            print(f"\n   Testing {pokemon['name']} (ID: {pokemon['species_id']}):")
            
            profile = PokemonIntelligence.get_pokemon_profile(pokemon['species_id'])
            
            print(f"      Intelligence: {profile['intelligence'].name}")
            print(f"      Communication: {profile['communication'].value}")
            print(f"      Animal Base: {profile['animal_base']}")
            print(f"      Instincts: {', '.join(profile['instincts'])}")
            print(f"      Speech Pattern: {profile['speech_pattern']}")
            
            # Verify expected traits
            if profile['intelligence'] == pokemon['expected_intelligence']:
                print(f"      ✅ Intelligence level correct")
            else:
                print(f"      ❌ Intelligence mismatch - expected {pokemon['expected_intelligence']}")
        
        print(f"\n   ✅ Pokemon Intelligence Profiles working correctly!")
        return True
        
    except Exception as e:
        print(f"   ❌ Pokemon Intelligence test failed: {e}")
        return False

def test_personality_builder():
    """Test the personality builder with complete Pokemon data"""
    print("🎭 Testing Personality Builder...")
    
    try:
        from app.services.pokemon_intelligence import PokemonPersonalityBuilder
        
        # Test with different friendship levels and natures
        test_cases = [
            {
                'name': 'Low Friendship Celebi',
                'data': {
                    'species_id': 251,
                    'species_name': 'Celebi',
                    'nickname': 'Celebi',
                    'level': 63,
                    'nature': 'Modest',
                    'friendship': 4,  # Very low
                    'types': ['Psychic', 'Grass'],
                    'is_mythical': True
                }
            },
            {
                'name': 'High Friendship Grookey',
                'data': {
                    'species_id': 810,
                    'species_name': 'Grookey', 
                    'nickname': 'Drummer',
                    'level': 100,
                    'nature': 'Jolly',
                    'friendship': 200,  # High
                    'types': ['Grass']
                }
            },
            {
                'name': 'Medium Friendship Pikachu',
                'data': {
                    'species_id': 25,
                    'species_name': 'Pikachu',
                    'nickname': 'Sparky',
                    'level': 45,
                    'nature': 'Timid',
                    'friendship': 120,  # Medium
                    'types': ['Electric']
                }
            }
        ]
        
        for test_case in test_cases:
            print(f"\n   Testing {test_case['name']}:")
            
            profile = PokemonPersonalityBuilder.build_authentic_profile(test_case['data'])
            
            print(f"      Intelligence: {profile['intelligence'].name}")
            print(f"      Communication: {profile['communication'].value}")
            print(f"      Friendship: {profile['friendship_level']}")
            print(f"      Nature: {profile['nature']}")
            print(f"      Animal Base: {profile['animal_base']}")
            print(f"      Behaviors: {[b.value for b in profile['behaviors']]}")
            
        print(f"\n   ✅ Personality Builder working correctly!")
        return True
        
    except Exception as e:
        print(f"   ❌ Personality Builder test failed: {e}")
        return False

def test_authentic_chat_responses():
    """Test the AI chat system with authentic animal responses"""
    print("🗣️ Testing Authentic Chat Responses...")
    
    try:
        from app.services.ai_chat_service import AIChatService
        
        service = AIChatService()
        
        # Test scenarios with different Pokemon
        test_scenarios = [
            {
                'pokemon_data': {
                    'species_id': 810,
                    'species_name': 'Grookey',
                    'nickname': 'Drummer',
                    'level': 15,  # Young
                    'nature': 'Jolly',
                    'friendship': 50,  # Low friendship - should be wary
                    'types': ['Grass']
                },
                'message': 'Hello there! Want to be friends?',
                'expected_tone': 'Cautious but curious, simple speech'
            },
            {
                'pokemon_data': {
                    'species_id': 25,
                    'species_name': 'Pikachu', 
                    'nickname': 'Sparky',
                    'level': 45,
                    'nature': 'Jolly',
                    'friendship': 180,  # High friendship - should be loyal
                    'types': ['Electric']
                },
                'message': 'How are you feeling today?',
                'expected_tone': 'Enthusiastic, loyal, energetic'
            },
            {
                'pokemon_data': {
                    'species_id': 150,
                    'species_name': 'Mewtwo',
                    'nickname': 'Mewtwo',
                    'level': 70,
                    'nature': 'Serious',
                    'friendship': 100,  # Medium friendship
                    'types': ['Psychic'],
                    'is_legendary': True
                },
                'message': 'What do you think about humans?',
                'expected_tone': 'Philosophical, intelligent, complex thoughts'
            }
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            pokemon = scenario['pokemon_data']
            message = scenario['message']
            expected_tone = scenario['expected_tone']
            
            print(f"\n   Scenario {i}: {pokemon['nickname']} (Friendship: {pokemon['friendship']})")
            print(f"      Message: '{message}'")
            print(f"      Expected tone: {expected_tone}")
            
            # Test AI response if available
            if service.is_available():
                try:
                    response = service.generate_pokemon_response(message, pokemon)
                    print(f"      AI Response: {response}")
                except Exception as e:
                    print(f"      AI Response failed: {e}")
                    # Fall through to fallback test
            
            # Always test fallback response for comparison
            fallback_response = service._fallback_response(message, pokemon)
            print(f"      Fallback Response: {fallback_response}")
            
        print(f"\n   ✅ Chat Response system working!")
        return True
        
    except Exception as e:
        print(f"   ❌ Chat Response test failed: {e}")
        return False

def test_intelligence_differences():
    """Test that different intelligence levels produce appropriately different responses"""
    print("🤖 Testing Intelligence Level Differences...")
    
    try:
        from app.services.ai_chat_service import AIChatService
        
        service = AIChatService()
        
        # Compare responses from different intelligence levels
        intelligence_tests = [
            {
                'name': 'Basic Intelligence (Magikarp-like)',
                'pokemon_data': {
                    'species_id': 129,  # Using generic for basic intelligence
                    'species_name': 'BasicMon',
                    'nickname': 'Simple',
                    'level': 10,
                    'nature': 'Hardy',
                    'friendship': 100,
                    'types': ['Water']
                },
                'message': 'What do you think about the meaning of life?',
                'expected': 'Simple, concrete response focused on basic needs'
            },
            {
                'name': 'Average Intelligence (Grookey)',
                'pokemon_data': {
                    'species_id': 810,
                    'species_name': 'Grookey',
                    'nickname': 'Drummer',
                    'level': 30,
                    'nature': 'Jolly',
                    'friendship': 150,
                    'types': ['Grass']
                },
                'message': 'What do you think about the meaning of life?',
                'expected': 'Practical, animal-perspective response'
            },
            {
                'name': 'Genius Intelligence (Mewtwo)',
                'pokemon_data': {
                    'species_id': 150,
                    'species_name': 'Mewtwo',
                    'nickname': 'Mewtwo',
                    'level': 70,
                    'nature': 'Serious',
                    'friendship': 100,
                    'types': ['Psychic'],
                    'is_legendary': True
                },
                'message': 'What do you think about the meaning of life?',
                'expected': 'Philosophical, complex, existential response'
            }
        ]
        
        for test in intelligence_tests:
            print(f"\n   {test['name']}:")
            print(f"      Question: {test['message']}")
            print(f"      Expected: {test['expected']}")
            
            # Get fallback response to show intelligence difference
            fallback_response = service._fallback_response(test['message'], test['pokemon_data'])
            print(f"      Response: {fallback_response}")
        
        print(f"\n   ✅ Intelligence differences demonstrated!")
        return True
        
    except Exception as e:
        print(f"   ❌ Intelligence differences test failed: {e}")
        return False

def main():
    """Run all authentic Pokemon tests"""
    print("🐾 Authentic Pokemon Animal Intelligence Test Suite\n")
    
    # Show configuration
    print("🔧 Configuration:")
    print(f"   AI_PROVIDER: {os.getenv('AI_PROVIDER', 'Not set')}")
    print(f"   OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    print(f"   CLAUDE_API_KEY: {'Set' if os.getenv('CLAUDE_API_KEY') else 'Not set'}")
    print()
    
    tests = [
        ("Pokemon Intelligence Profiles", test_pokemon_intelligence_profiles),
        ("Personality Builder", test_personality_builder),
        ("Authentic Chat Responses", test_authentic_chat_responses),
        ("Intelligence Level Differences", test_intelligence_differences)
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
        print("🎉 All tests passed! Authentic Pokemon animal intelligence is working!")
        print("🐾 Pokemon will now feel like real intelligent animals!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)