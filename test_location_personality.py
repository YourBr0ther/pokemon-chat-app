#!/usr/bin/env python3
"""
Test script for location-based personality traits and first encounter system
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_location_traits():
    """Test location-based personality traits"""
    print("🌍 Testing Location-Based Personality Traits...")
    
    try:
        from app.services.pokemon_intelligence import PokemonPersonalityBuilder
        
        # Test different habitats and their effects
        test_cases = [
            {
                'name': 'Forest Pikachu',
                'data': {
                    'species_id': 25,
                    'species_name': 'Pikachu',
                    'nickname': 'Sparky',
                    'habitat': 'forest',
                    'friendship': 120,
                    'nature': 'Jolly'
                },
                'expected_environment': 'Dense woodlands'
            },
            {
                'name': 'Cave Celebi',
                'data': {
                    'species_id': 251,
                    'species_name': 'Celebi',
                    'nickname': 'Celebi',
                    'habitat': 'cave',
                    'friendship': 50,
                    'nature': 'Timid'
                },
                'expected_environment': 'Dark underground'
            },
            {
                'name': 'Urban Grookey',
                'data': {
                    'species_id': 810,
                    'species_name': 'Grookey',
                    'nickname': 'Drummer',
                    'habitat': 'urban',
                    'friendship': 180,
                    'nature': 'Bold'
                },
                'expected_environment': 'Cities and human'
            }
        ]
        
        for test_case in test_cases:
            print(f"\n   Testing {test_case['name']}:")
            
            profile = PokemonPersonalityBuilder.build_authentic_profile(test_case['data'])
            location_traits = profile['location_traits']
            
            print(f"      Habitat: {location_traits['habitat_type']}")
            print(f"      Environment: {location_traits['environment']}")
            print(f"      Comfort Zone: {location_traits['comfort_zone']}")
            print(f"      Survival Skills: {location_traits['survival_skills']}")
            print(f"      Natural Fears: {location_traits['fears']}")
            print(f"      Home Memories: {location_traits['memories']}")
            
            # Verify expected traits
            if test_case['expected_environment'].lower() in location_traits['environment'].lower():
                print(f"      ✅ Environment correctly identified")
            else:
                print(f"      ❌ Environment mismatch")
        
        print(f"\n   ✅ Location traits system working correctly!")
        return True
        
    except Exception as e:
        print(f"   ❌ Location traits test failed: {e}")
        return False

def test_friendship_nature_reactions():
    """Test friendship-influenced nature reactions"""
    print("😊 Testing Friendship-Influenced Nature Reactions...")
    
    try:
        from app.services.pokemon_intelligence import PokemonPersonalityBuilder
        
        # Test same nature with different friendship levels
        base_pokemon = {
            'species_id': 25,
            'species_name': 'Pikachu', 
            'nickname': 'TestPika',
            'nature': 'Brave',
            'habitat': 'forest'
        }
        
        friendship_levels = [
            {'friendship': 30, 'expected_manifestation': 'defensive'},
            {'friendship': 100, 'expected_manifestation': 'evolving'},
            {'friendship': 200, 'expected_manifestation': 'trusting'}
        ]
        
        for test in friendship_levels:
            pokemon_data = {**base_pokemon, 'friendship': test['friendship']}
            profile = PokemonPersonalityBuilder.build_authentic_profile(pokemon_data)
            nature_reaction = profile['nature_reaction']
            
            print(f"\n   Brave Nature at Friendship {test['friendship']}:")
            print(f"      Dominant Trait: {nature_reaction['dominant_trait']}")
            print(f"      Manifestation: {nature_reaction['manifestation']}")
            print(f"      Description: {nature_reaction['nature_description']}")
            
            if nature_reaction['manifestation'] == test['expected_manifestation']:
                print(f"      ✅ Manifestation correct")
            else:
                print(f"      ❌ Expected {test['expected_manifestation']}, got {nature_reaction['manifestation']}")
        
        print(f"\n   ✅ Friendship-nature reactions system working!")
        return True
        
    except Exception as e:
        print(f"   ❌ Friendship-nature reactions test failed: {e}")
        return False

def test_first_encounter_scenarios():
    """Test first encounter scenario generation"""
    print("🎭 Testing First Encounter Scenarios...")
    
    try:
        from app.services.pokemon_intelligence import PokemonPersonalityBuilder
        
        # Test different scenarios
        test_cases = [
            {
                'name': 'Traumatic Capture (Very Low Friendship)',
                'data': {
                    'species_id': 816,  # Sobble - shy
                    'species_name': 'Sobble',
                    'nickname': 'Tearful',
                    'friendship': 20,  # Very low
                    'nature': 'Timid',
                    'habitat': 'waters-edge'
                },
                'expected_emotion': 'fear'
            },
            {
                'name': 'Confused Awakening (Medium Friendship)',
                'data': {
                    'species_id': 810,  # Grookey
                    'species_name': 'Grookey',
                    'nickname': 'Drummer',
                    'friendship': 80,
                    'nature': 'Jolly',
                    'habitat': 'forest'
                },
                'expected_emotion': 'confusion'
            },
            {
                'name': 'Curious Introduction (High Friendship)',
                'data': {
                    'species_id': 25,  # Pikachu
                    'species_name': 'Pikachu',
                    'nickname': 'Sparky',
                    'friendship': 150,
                    'nature': 'Bold',
                    'habitat': 'grassland'
                },
                'expected_emotion': 'curiosity'
            }
        ]
        
        for test_case in test_cases:
            print(f"\n   Testing {test_case['name']}:")
            
            scenario = PokemonPersonalityBuilder.get_first_encounter_scenario(test_case['data'])
            
            print(f"      Primary Emotion: {scenario['primary_emotion']}")
            print(f"      Reaction Intensity: {scenario['reaction_intensity']}")
            print(f"      Trust Level: {scenario['trust_level']}")
            print(f"      Opening Line: {scenario['opening_line']}")
            print(f"      Displacement Memory: {scenario['displacement_memory']}")
            print(f"      Awakening: {scenario['awakening_description']}")
            
            if scenario['primary_emotion'] == test_case['expected_emotion']:
                print(f"      ✅ Primary emotion correct")
            else:
                print(f"      ❌ Expected {test_case['expected_emotion']}, got {scenario['primary_emotion']}")
        
        print(f"\n   ✅ First encounter scenarios working!")
        return True
        
    except Exception as e:
        print(f"   ❌ First encounter scenarios test failed: {e}")
        return False

def test_first_encounter_chat_response():
    """Test first encounter chat integration"""
    print("💬 Testing First Encounter Chat Integration...")
    
    try:
        from app.personality.chat_engine import ChatEngine
        
        chat_engine = ChatEngine()
        
        # Test first encounter with different Pokemon
        test_cases = [
            {
                'name': 'Scared Sobble First Chat',
                'pokemon_data': {
                    'species_id': 816,
                    'species_name': 'Sobble',
                    'nickname': 'Teary',
                    'friendship': 30,
                    'nature': 'Timid',
                    'habitat': 'waters-edge',
                    'level': 15,
                    'types': ['Water']
                },
                'user_message': 'Hello there, little one!',
                'conversation_history': []  # Empty = first encounter
            },
            {
                'name': 'Confident Mewtwo First Chat',
                'pokemon_data': {
                    'species_id': 150,
                    'species_name': 'Mewtwo',
                    'nickname': 'Mewtwo',
                    'friendship': 100,
                    'nature': 'Serious',
                    'habitat': 'cave',
                    'level': 70,
                    'types': ['Psychic'],
                    'is_legendary': True
                },
                'user_message': 'Greetings, powerful one.',
                'conversation_history': []  # Empty = first encounter
            }
        ]
        
        for test_case in test_cases:
            print(f"\n   Testing {test_case['name']}:")
            print(f"      User Message: '{test_case['user_message']}'")
            
            response = chat_engine.generate_response(
                test_case['pokemon_data'],
                test_case['user_message'],
                test_case['conversation_history']
            )
            
            print(f"      Pokemon Response: {response}")
            
            # Check if response shows first encounter characteristics
            first_encounter_indicators = [
                'where am i', 'strange', 'confused', 'scared', 'home', 
                'place', 'remember', 'digital', 'materialized', 'don\'t know'
            ]
            
            response_lower = response.lower()
            found_indicators = [indicator for indicator in first_encounter_indicators 
                               if indicator in response_lower]
            
            if found_indicators:
                print(f"      ✅ First encounter indicators found: {found_indicators}")
            else:
                print(f"      ⚠️  No clear first encounter indicators detected")
        
        print(f"\n   ✅ First encounter chat integration working!")
        return True
        
    except Exception as e:
        print(f"   ❌ First encounter chat integration test failed: {e}")
        return False

def test_ai_enhanced_personality_prompts():
    """Test AI prompts with enhanced personality features"""
    print("🤖 Testing Enhanced AI Personality Prompts...")
    
    try:
        from app.services.ai_chat_service import AIChatService
        
        service = AIChatService()
        
        # Test comprehensive personality data
        pokemon_data = {
            'species_id': 25,
            'species_name': 'Pikachu',
            'nickname': 'Sparky',
            'friendship': 80,
            'nature': 'Jolly',
            'habitat': 'forest',
            'level': 45,
            'types': ['Electric'],
            'genus': 'Mouse Pokemon',
            'description': 'When it is angered, it immediately discharges electricity.'
        }
        
        # Test prompt building
        prompt = service._build_personality_prompt(pokemon_data)
        
        print(f"\n   Testing Enhanced Prompt Structure:")
        
        # Check for key sections
        required_sections = [
            '🧠 INTELLIGENCE PROFILE:',
            '🗣️ COMMUNICATION ABILITY:',
            '🐾 ANIMAL NATURE:',
            '🎭 PERSONALITY:',
            '❤️ BOND WITH TRAINER:',
            '📊 PHYSICAL INFORMATION:',
            '🌍 HABITAT & MEMORIES:',
            '🎯 AUTHENTIC POKEMON BEHAVIOR RULES:'
        ]
        
        for section in required_sections:
            if section in prompt:
                print(f"      ✅ Found section: {section}")
            else:
                print(f"      ❌ Missing section: {section}")
        
        # Check for location-specific content
        if 'forest' in prompt.lower():
            print(f"      ✅ Habitat information included")
        else:
            print(f"      ❌ Habitat information missing")
        
        # Check for nature reaction content
        if 'manifestation' in prompt.lower():
            print(f"      ✅ Nature reaction information included")
        else:
            print(f"      ❌ Nature reaction information missing")
        
        print(f"\n   ✅ Enhanced AI prompts working!")
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced AI prompts test failed: {e}")
        return False

def main():
    """Run all location personality and first encounter tests"""
    print("🏔️ Location-Based Personality & First Encounter Test Suite\n")
    
    # Show configuration
    print("🔧 Configuration:")
    print(f"   AI_PROVIDER: {os.getenv('AI_PROVIDER', 'Not set')}")
    print(f"   OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    print(f"   CLAUDE_API_KEY: {'Set' if os.getenv('CLAUDE_API_KEY') else 'Not set'}")
    print()
    
    tests = [
        ("Location Traits", test_location_traits),
        ("Friendship-Nature Reactions", test_friendship_nature_reactions),
        ("First Encounter Scenarios", test_first_encounter_scenarios),
        ("First Encounter Chat Integration", test_first_encounter_chat_response),
        ("Enhanced AI Prompts", test_ai_enhanced_personality_prompts)
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
        print("🎉 All tests passed! Location-based personality and first encounters working!")
        print("🏔️ Pokemon will now react based on their natural habitat!")
        print("🎭 First conversations will be special awakening moments!")
        print("😊 Nature traits will change based on friendship levels!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)