#!/usr/bin/env python3
"""
Test script to verify PokeAPI integration is working correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.services.pokeapi_service import PokeAPIService
from app.parsers.pk8_parser import PK8Parser

def test_pokeapi_service():
    """Test PokeAPI service functionality"""
    print("🧪 Testing PokeAPI Service...")
    
    service = PokeAPIService()
    
    # Test with Celebi (251)
    print("   Testing Celebi (ID: 251)...")
    celebi_data = service.get_pokemon_data(251)
    
    if celebi_data:
        print(f"   ✅ Celebi data retrieved:")
        print(f"      - Name: {celebi_data['name']}")
        print(f"      - Genus: {celebi_data.get('genus', 'N/A')}")
        print(f"      - Description: {celebi_data.get('flavor_text', 'N/A')[:50]}...")
        print(f"      - Legendary: {celebi_data.get('is_legendary', False)}")
        print(f"      - Mythical: {celebi_data.get('is_mythical', False)}")
        print(f"      - Sprite URL: {celebi_data['sprites']['front_default']}")
    else:
        print("   ❌ Failed to retrieve Celebi data")
        return False
    
    # Test with Grookey (810)
    print("   Testing Grookey (ID: 810)...")
    grookey_data = service.get_pokemon_data(810)
    
    if grookey_data:
        print(f"   ✅ Grookey data retrieved:")
        print(f"      - Name: {grookey_data['name']}")
        print(f"      - Types: {grookey_data.get('types', [])}")
        print(f"      - Genus: {grookey_data.get('genus', 'N/A')}")
        print(f"      - Height: {grookey_data.get('height', 0)} decimeters")
        print(f"      - Weight: {grookey_data.get('weight', 0)} hectograms")
    else:
        print("   ❌ Failed to retrieve Grookey data")
        return False
    
    return True

def test_parser_integration():
    """Test PK8 parser with PokeAPI integration"""
    print("🧪 Testing PK8 Parser Integration...")
    
    parser = PK8Parser()
    
    # Test species recognition
    print("   Testing species recognition...")
    celebi_name = parser.SPECIES_NAMES.get(251, "Unknown")
    grookey_name = parser.SPECIES_NAMES.get(810, "Unknown")
    
    print(f"   ✅ Species 251: {celebi_name}")
    print(f"   ✅ Species 810: {grookey_name}")
    
    # Test type mapping
    print("   Testing type mapping...")
    celebi_types = parser._get_pokemon_types(251)
    grookey_types = parser._get_pokemon_types(810)
    
    print(f"   ✅ Celebi types: {celebi_types}")
    print(f"   ✅ Grookey types: {grookey_types}")
    
    return True

def test_database_schema():
    """Test database schema with new columns"""
    print("🧪 Testing Database Schema...")
    
    app = create_app()
    
    with app.app_context():
        from app.models.pokemon import db, Pokemon
        
        # Check if we can create a Pokemon instance with new fields
        try:
            test_pokemon = Pokemon(
                species_id=251,
                species_name="Celebi",
                nickname="Test Celebi",
                level=50,
                nature="Modest",
                friendship=100,
                original_trainer="Tester",
                # New PokeAPI fields
                sprite_url="https://example.com/sprite.png",
                description="Test description",
                genus="Time Travel Pokémon",
                height=60,
                weight=50,
                is_legendary=False,
                is_mythical=True
            )
            
            # Set complex fields
            test_pokemon.set_types(["Psychic", "Grass"])
            test_pokemon.set_ivs({"hp": 31, "attack": 31, "defense": 31, "sp_attack": 31, "sp_defense": 31, "speed": 31})
            test_pokemon.set_abilities([{"name": "natural-cure", "is_hidden": False}])
            test_pokemon.set_base_stats({"hp": 100, "attack": 100, "defense": 100, "special-attack": 100, "special-defense": 100, "speed": 100})
            
            print("   ✅ Pokemon model created successfully with new fields")
            print(f"   ✅ Best sprite: {test_pokemon.get_best_sprite()}")
            print(f"   ✅ Height formatted: {test_pokemon.get_height_formatted()}")
            print(f"   ✅ Weight formatted: {test_pokemon.get_weight_formatted()}")
            
            # Test to_dict method
            pokemon_dict = test_pokemon.to_dict()
            new_fields = ['sprite_url', 'description', 'genus', 'height', 'weight', 'is_legendary', 'is_mythical']
            
            for field in new_fields:
                if field in pokemon_dict:
                    print(f"   ✅ {field} in dict: {pokemon_dict[field]}")
                else:
                    print(f"   ❌ {field} missing from dict")
                    return False
                    
            return True
            
        except Exception as e:
            print(f"   ❌ Database schema test failed: {e}")
            return False

def main():
    """Run all tests"""
    print("🚀 Starting PokeAPI Integration Test Suite...\n")
    
    tests = [
        ("PokeAPI Service", test_pokeapi_service),
        ("Parser Integration", test_parser_integration),
        ("Database Schema", test_database_schema)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🔍 Running {test_name} test...")
        try:
            if test_func():
                print(f"✅ {test_name} test PASSED\n")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PokeAPI integration is working correctly!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)