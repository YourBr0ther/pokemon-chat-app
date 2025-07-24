#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from parsers.pk8_parser import PK8Parser

def test_celebi_parsing():
    print("Testing PK8 Parser with Celebi file...")
    
    parser = PK8Parser()
    
    try:
        # Parse the Celebi file
        pokemon_data = parser.parse_file('test_celebi.pk8')
        personality_traits = parser.get_personality_traits(pokemon_data)
        
        print("\n=== Pokemon Data ===")
        for key, value in pokemon_data.items():
            print(f"{key}: {value}")
        
        print("\n=== Personality Traits ===")
        for key, value in personality_traits.items():
            print(f"{key}: {value}")
        
        print("\n✅ Parser test successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Parser test failed: {e}")
        return False

if __name__ == '__main__':
    test_celebi_parsing()