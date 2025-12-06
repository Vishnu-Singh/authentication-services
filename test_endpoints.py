#!/usr/bin/env python
"""
Test script to verify authentication service endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_session_registration():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    url = f"{BASE_URL}/api/auth/session/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201, 400]  # 400 if user exists
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_jwt_token():
    """Test JWT token generation"""
    print("\n=== Testing JWT Token Generation ===")
    url = f"{BASE_URL}/api/token/"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            tokens = response.json()
            print(f"Access Token: {tokens.get('access', '')[:50]}...")
            return tokens.get('access')
        else:
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_api_endpoints():
    """Test various API endpoints"""
    print("\n=== Testing API Endpoints ===")
    
    endpoints = [
        ("GET", "/api/auth/oauth/.well-known/openid-configuration/"),
        ("GET", "/api/auth/saml/metadata/"),
    ]
    
    for method, endpoint in endpoints:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n{method} {endpoint}")
        try:
            if method == "GET":
                response = requests.get(url)
            else:
                response = requests.post(url)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✓ Endpoint accessible")
            else:
                print(f"Response: {response.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")


def main():
    print("=" * 60)
    print("Authentication Service Test Suite")
    print("=" * 60)
    print("\nNote: Make sure the Django server is running on localhost:8000")
    
    # Test registration
    test_session_registration()
    
    # Test JWT tokens
    access_token = test_jwt_token()
    
    # Test public endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
