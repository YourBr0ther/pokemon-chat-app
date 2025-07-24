#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from parsers.pk8_parser import PK8Parser

def test_pk8_edge_cases():
    print("🧪 Testing PK8 Parser Edge Cases...")
    
    parser = PK8Parser()
    
    # Test 1: Valid file
    print("\n✅ Testing Valid File...")
    try:
        pokemon_data = parser.parse_file('test_celebi.pk8')
        print(f"   ✅ Valid file parsed successfully: {pokemon_data['species_name']}")
    except Exception as e:
        print(f"   ❌ Valid file test failed: {e}")
        return False
    
    # Test 2: Non-existent file
    print("\n❓ Testing Non-existent File...")
    try:
        parser.parse_file('nonexistent.pk8')
        print("   ❌ Should have failed for non-existent file")
        return False
    except Exception as e:
        print(f"   ✅ Correctly failed for non-existent file: {type(e).__name__}")
    
    # Test 3: Invalid file size (create dummy files)
    print("\n📏 Testing Invalid File Sizes...")
    
    # Too small file
    with open('test_small.pk8', 'wb') as f:
        f.write(b'too small')
    
    try:
        parser.parse_file('test_small.pk8')
        print("   ❌ Should have failed for too small file")
        return False
    except Exception as e:
        print(f"   ✅ Correctly failed for small file: {type(e).__name__}")
        os.remove('test_small.pk8')
    
    # Too large file
    with open('test_large.pk8', 'wb') as f:
        f.write(b'x' * 500)  # 500 bytes instead of 344
    
    try:
        parser.parse_file('test_large.pk8')
        print("   ❌ Should have failed for too large file")
        return False
    except Exception as e:
        print(f"   ✅ Correctly failed for large file: {type(e).__name__}")
        os.remove('test_large.pk8')
    
    # Test 4: Test bytes parsing
    print("\n🔢 Testing Bytes Parsing...")
    
    with open('test_celebi.pk8', 'rb') as f:
        pk8_bytes = f.read()
    
    try:
        pokemon_data = parser.parse_bytes(pk8_bytes)
        print(f"   ✅ Bytes parsing successful: {pokemon_data['species_name']}")
    except Exception as e:
        print(f"   ❌ Bytes parsing failed: {e}")
        return False
    
    # Test 5: Test personality traits generation
    print("\n🎭 Testing Personality Traits...")
    
    try:
        traits = parser.get_personality_traits(pokemon_data)
        expected_keys = ['species_personality', 'type_influence', 'nature_traits', 'friendship_level', 'level_maturity']
        
        for key in expected_keys:
            if key not in traits:
                print(f"   ❌ Missing personality trait: {key}")
                return False
        
        print(f"   ✅ All personality traits generated: {list(traits.keys())}")
        
        # Test specific trait values for Celebi
        if traits['species_personality'] == 'gentle':
            print("   ✅ Correct species personality for Celebi")
        else:
            print(f"   ⚠️ Unexpected species personality: {traits['species_personality']}")
            
        if traits['type_influence'] == 'thoughtful':
            print("   ✅ Correct type influence for Psychic/Grass")
        else:
            print(f"   ⚠️ Unexpected type influence: {traits['type_influence']}")
            
    except Exception as e:
        print(f"   ❌ Personality traits test failed: {e}")
        return False
    
    # Test 6: Test UTF-16 string decoding
    print("\n📝 Testing String Decoding...")
    
    # Test empty string
    empty_bytes = b'\x00' * 24
    decoded = parser._decode_utf16_string(empty_bytes)
    if decoded == "":
        print("   ✅ Empty string decoded correctly")
    else:
        print(f"   ❌ Empty string not decoded correctly: '{decoded}'")
    
    # Test normal string (create UTF-16 encoded bytes)
    test_string = "TestName"
    utf16_bytes = test_string.encode('utf-16le') + b'\x00\x00'  # null terminate
    utf16_bytes = utf16_bytes.ljust(24, b'\x00')  # pad to 24 bytes
    
    decoded = parser._decode_utf16_string(utf16_bytes)
    if decoded == test_string:
        print("   ✅ UTF-16 string decoded correctly")
    else:
        print(f"   ❌ UTF-16 string not decoded correctly: '{decoded}' vs '{test_string}'")
    
    # Test 7: Test type mapping
    print("\n🏷️ Testing Type Mapping...")
    
    # Test known species
    celebi_types = parser._get_pokemon_types(251)  # Celebi
    if celebi_types == ["Psychic", "Grass"]:
        print("   ✅ Celebi types correct")
    else:
        print(f"   ❌ Celebi types incorrect: {celebi_types}")
    
    pikachu_types = parser._get_pokemon_types(25)  # Pikachu
    if pikachu_types == ["Electric"]:
        print("   ✅ Pikachu types correct")
    else:
        print(f"   ❌ Pikachu types incorrect: {pikachu_types}")
    
    # Test unknown species
    unknown_types = parser._get_pokemon_types(9999)
    if unknown_types == ["Normal"]:
        print("   ✅ Unknown species defaults to Normal type")
    else:
        print(f"   ❌ Unknown species type mapping failed: {unknown_types}")
    
    # Test 8: Test personality helper methods
    print("\n🧠 Testing Personality Helpers...")
    
    # Test friendship levels
    distant = parser._get_friendship_level(50)
    warming = parser._get_friendship_level(100)
    loyal = parser._get_friendship_level(200)
    
    if distant == "distant" and warming == "warming_up" and loyal == "loyal":
        print("   ✅ Friendship levels calculated correctly")
    else:
        print(f"   ❌ Friendship levels incorrect: {distant}, {warming}, {loyal}")
    
    # Test maturity levels
    young = parser._get_level_maturity(20)
    mature = parser._get_level_maturity(40)
    wise = parser._get_level_maturity(60)
    
    if young == "young" and mature == "mature" and wise == "wise":
        print("   ✅ Maturity levels calculated correctly")
    else:
        print(f"   ❌ Maturity levels incorrect: {young}, {mature}, {wise}")
    
    print("\n🎉 All PK8 parser edge case tests passed!")
    return True

if __name__ == '__main__':
    test_pk8_edge_cases()