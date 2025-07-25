#!/usr/bin/env python3
"""
Test script to verify security improvements are working correctly
"""

import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_csrf_protection():
    """Test that CSRF protection is working"""
    print("Testing CSRF protection...")
    app = create_app()
    
    with app.test_client() as client:
        # Test that POST without CSRF token fails
        response = client.post('/api/save', 
                             json={'pokemon_data': {'test': 'data'}},
                             headers={'Content-Type': 'application/json'})
        
        if response.status_code == 403:
            print("✅ CSRF protection working - POST without token rejected")
            return True
        else:
            print(f"❌ CSRF protection failed - got status {response.status_code}")
            return False

def test_input_validation():
    """Test that input validation schemas are working"""
    print("Testing input validation...")
    app = create_app()
    
    with app.test_client() as client:
        # Get CSRF token first
        response = client.get('/')
        
        # Test invalid message data
        response = client.post('/api/pokemon/1/send',
                             json={'message': ''},  # Empty message should fail
                             headers={'Content-Type': 'application/json'})
        
        if response.status_code == 400:
            print("✅ Input validation working - empty message rejected")
            return True
        else:
            print(f"❌ Input validation failed - got status {response.status_code}")
            return False

def test_rate_limiting():
    """Test that rate limiting is configured"""
    print("Testing rate limiting configuration...")
    app = create_app()
    
    # Check if limiter is configured
    from app.extensions import limiter
    if limiter:
        print("✅ Rate limiter is configured")
        return True
    else:
        print("❌ Rate limiter not found")
        return False

def main():
    """Run all security tests"""
    print("🔐 Running Security Improvement Tests")
    print("=" * 40)
    
    tests = [
        test_csrf_protection,
        test_input_validation, 
        test_rate_limiting
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("=" * 40)
    print(f"Security Tests: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All security improvements are working!")
        return 0
    else:
        print("⚠️  Some security improvements need attention")
        return 1

if __name__ == "__main__":
    exit(main())