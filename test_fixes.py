#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from parsers.pk8_parser import PK8Parser

def test_file_size_flexibility():
    print("🧪 Testing File Size Flexibility...")
    
    parser = PK8Parser()
    
    # Test 1: Create different sized files to test flexibility
    test_sizes = [320, 344, 368]  # Slightly different sizes
    
    for size in test_sizes:
        print(f"\nTesting {size} byte file:")
        
        # Create a test file with that size
        with open('test_celebi.pk8', 'rb') as f:
            original_data = f.read()
        
        if size < len(original_data):
            # Truncate
            test_data = original_data[:size]
        else:
            # Pad with zeros
            test_data = original_data + b'\x00' * (size - len(original_data))
        
        try:
            result = parser.parse_bytes(test_data)
            print(f"   ✅ {size} bytes: Parsed successfully")
            print(f"      Species: {result['species_name']}")
            print(f"      Level: {result['level']}")
            print(f"      Nature: {result['nature']}")
            
            # Validate ranges
            valid = True
            if not (1 <= result['level'] <= 100):
                print(f"      ❌ Invalid level: {result['level']}")
                valid = False
            
            for stat, value in result['ivs'].items():
                if not (0 <= value <= 31):
                    print(f"      ❌ Invalid IV {stat}: {value}")
                    valid = False
            
            if valid:
                print(f"      ✅ All values within valid ranges")
            
        except Exception as e:
            print(f"   ❌ {size} bytes: Failed - {e}")
    
    # Test 2: Test files that should be rejected
    print(f"\nTesting files that should be rejected:")
    
    invalid_sizes = [200, 500]  # Too small, too large
    
    for size in invalid_sizes:
        test_data = b'\x00' * size
        try:
            parser.parse_bytes(test_data)
            print(f"   ❌ {size} bytes: Should have been rejected but wasn't")
        except Exception as e:
            print(f"   ✅ {size} bytes: Correctly rejected - {str(e)[:50]}...")

def test_robust_parsing():
    print(f"\n🔧 Testing Robust Parsing with Original Celebi...")
    
    parser = PK8Parser()
    
    try:
        result = parser.parse_file('test_celebi.pk8')
        
        print(f"✅ Parsing successful:")
        print(f"   Species: {result['species_name']} (ID: {result['species_id']})")
        print(f"   Level: {result['level']}")
        print(f"   Nature: {result['nature']}")
        print(f"   Friendship: {result['friendship']}")
        print(f"   IVs: {result['ivs']}")
        
        # Validate all are reasonable
        issues = []
        
        if not (1 <= result['level'] <= 100):
            issues.append(f"Invalid level: {result['level']}")
        
        if not (0 <= result['friendship'] <= 255):
            issues.append(f"Invalid friendship: {result['friendship']}")
            
        for stat, value in result['ivs'].items():
            if not (0 <= value <= 31):
                issues.append(f"Invalid IV {stat}: {value}")
        
        if issues:
            print(f"❌ Issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ All values are within valid Pokemon ranges!")
            
        return len(issues) == 0
        
    except Exception as e:
        print(f"❌ Parsing failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Testing PK8 Parser Fixes...")
    
    size_test = test_file_size_flexibility()
    parse_test = test_robust_parsing()
    
    if parse_test:
        print(f"\n🎉 Parser fixes are working correctly!")
    else:
        print(f"\n❌ Parser still has issues.")