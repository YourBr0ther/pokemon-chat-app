#!/usr/bin/env python3
"""
Demonstration of enhanced Pokemon personality features:
- Location-based memories and traits
- Friendship-influenced nature reactions
- First encounter awakening scenarios
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def demo_enhanced_features():
    """Demonstrate the enhanced Pokemon personality features"""
    print("🌟 Enhanced Pokemon Personality Features Demo\n")
    
    try:
        from app.services.pokemon_intelligence import PokemonPersonalityBuilder
        from app.personality.chat_engine import ChatEngine
        
        chat_engine = ChatEngine()
        
        # Demo 1: Same Pokemon in different habitats
        print("🏔️ DEMO 1: Location Influence on Personality")
        print("=" * 50)
        
        base_pikachu = {
            'species_id': 25,
            'species_name': 'Pikachu',
            'nickname': 'Sparky',
            'friendship': 100,
            'nature': 'Jolly',
            'level': 30,
            'types': ['Electric']
        }
        
        habitats = ['forest', 'cave', 'urban']
        
        for habitat in habitats:
            pokemon_data = {**base_pikachu, 'habitat': habitat}
            profile = PokemonPersonalityBuilder.build_authentic_profile(pokemon_data)
            location_traits = profile['location_traits']
            
            print(f"\n🌍 Pikachu from {habitat.title()}:")
            print(f"   Environment: {location_traits['environment']}")
            print(f"   Comfort Zone: {location_traits['comfort_zone']}")
            print(f"   Home Memories: {location_traits['memories']}")
            
        # Demo 2: Friendship affecting nature expression
        print("\n\n😊 DEMO 2: Friendship Influence on Nature")
        print("=" * 50)
        
        brave_pokemon = {
            'species_id': 810,
            'species_name': 'Grookey',
            'nickname': 'Drummer',
            'nature': 'Brave',
            'habitat': 'forest',
            'level': 25,
            'types': ['Grass']
        }
        
        friendship_levels = [30, 100, 200]
        
        for friendship in friendship_levels:
            pokemon_data = {**brave_pokemon, 'friendship': friendship}
            profile = PokemonPersonalityBuilder.build_authentic_profile(pokemon_data)
            nature_reaction = profile['nature_reaction']
            
            print(f"\n❤️ Brave Grookey with {friendship} Friendship:")
            print(f"   Manifestation: {nature_reaction['manifestation'].title()}")
            print(f"   Dominant Trait: {nature_reaction['dominant_trait']}")
        
        # Demo 3: First encounter scenarios
        print("\n\n🎭 DEMO 3: First Encounter Awakening")
        print("=" * 50)
        
        first_encounter_pokemon = [
            {
                'species_id': 816,
                'species_name': 'Sobble',
                'nickname': 'Tearful',
                'friendship': 25,  # Very scared
                'nature': 'Timid',
                'habitat': 'waters-edge',
                'level': 10,
                'types': ['Water']
            },
            {
                'species_id': 150,
                'species_name': 'Mewtwo',
                'nickname': 'Mewtwo',
                'friendship': 120,  # Cautious but not hostile
                'nature': 'Serious',
                'habitat': 'cave',
                'level': 70,
                'types': ['Psychic'],
                'is_legendary': True
            }
        ]
        
        for pokemon_data in first_encounter_pokemon:
            scenario = PokemonPersonalityBuilder.get_first_encounter_scenario(pokemon_data)
            
            print(f"\n🌟 {pokemon_data['nickname']} First Awakening:")
            print(f"   Primary Emotion: {scenario['primary_emotion'].title()}")
            print(f"   Opening Line: \"{scenario['opening_line']}\"")
            print(f"   Displacement Memory: \"{scenario['displacement_memory']}\"")
            
            # Show first chat response
            first_response = chat_engine.generate_response(
                pokemon_data, 
                "Hello there, I'm your trainer.", 
                []  # Empty conversation history = first encounter
            )
            
            print(f"   First Chat Response:")
            print(f"   \"{first_response[:150]}...\"")
        
        # Demo 4: Comprehensive personality comparison
        print("\n\n🧠 DEMO 4: Complete Personality Profile")
        print("=" * 50)
        
        demo_pokemon = {
            'species_id': 25,
            'species_name': 'Pikachu',
            'nickname': 'Sparky',
            'friendship': 150,
            'nature': 'Jolly',
            'habitat': 'forest',
            'level': 45,
            'types': ['Electric'],
            'genus': 'Mouse Pokemon',
            'description': 'Stores electricity in its cheek pouches.'
        }
        
        profile = PokemonPersonalityBuilder.build_authentic_profile(demo_pokemon)
        
        print(f"\n⚡ Complete Profile for {profile['nickname']}:")
        print(f"   Intelligence Level: {profile['intelligence'].name}")
        print(f"   Communication Style: {profile['communication'].value}")
        print(f"   Animal Base: {profile['animal_base']}")
        print(f"   Speech Pattern: {profile['speech_pattern']}")
        print(f"   Nature Manifestation: {profile['nature_reaction']['manifestation']}")
        print(f"   Habitat: {profile['location_traits']['habitat_type']}")
        print(f"   Home Memories: {profile['location_traits']['memories']}")
        
        print("\n🎉 Enhanced Features Demo Complete!")
        print("\nKey Improvements:")
        print("✅ Pokemon now have location-based memories and fears")
        print("✅ Nature traits change based on friendship (negative when wary, positive when trusting)")
        print("✅ First conversations are special awakening moments with displacement confusion")
        print("✅ Each Pokemon feels authentically tied to their natural habitat")
        print("✅ Friendship evolution affects how Pokemon express their nature")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_enhanced_features()
    sys.exit(0 if success else 1)