"""
Test script to verify API endpoints.
Run: python scripts/test_api.py
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

# Store tokens for authenticated requests
access_token = None
refresh_token = None


def log_response(response, title="Response"):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def get_headers():
    """Get headers with auth token."""
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers


def test_health():
    """Test health endpoint."""
    print("\n🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    log_response(response, "Health Check")
    assert response.status_code == 200


def test_register():
    """Test user registration."""
    print("\n🔍 Testing User Registration...")
    data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpass123456",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data, headers=get_headers())
    log_response(response, "Register User")
    assert response.status_code == 201


def test_login():
    """Test user login."""
    global access_token, refresh_token
    
    print("\n🔍 Testing User Login...")
    data = {
        "email": "testuser@example.com",
        "password": "testpass123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    log_response(response, "Login")
    assert response.status_code == 200
    
    result = response.json()
    access_token = result["access_token"]
    refresh_token = result["refresh_token"]
    print(f"\n✓ Got access token: {access_token[:20]}...")


def test_get_current_user():
    """Test get current user."""
    print("\n🔍 Testing Get Current User...")
    response = requests.get(f"{BASE_URL}/auth/me", headers=get_headers())
    log_response(response, "Get Current User")
    assert response.status_code == 200


def test_create_product():
    """Test create product."""
    print("\n🔍 Testing Create Product...")
    data = {
        "name": "Test T-Shirt",
        "brand": "TestBrand",
        "category": "tops",
        "price": 29.99,
        "image_url": "https://example.com/test.jpg",
        "description": "Test product",
        "color": "blue",
        "fabric_type": "cotton"
    }
    response = requests.post(
        f"{BASE_URL}/products/",
        json=data,
        headers=get_headers()
    )
    log_response(response, "Create Product")
    # Should be 403 without proper role
    if response.status_code in [201, 403]:
        print("✓ Product endpoint working (role check)")


def test_list_products():
    """Test list products."""
    print("\n🔍 Testing List Products...")
    response = requests.get(f"{BASE_URL}/products/", headers=get_headers())
    log_response(response, "List Products")
    assert response.status_code == 200


def test_get_trending():
    """Test trending outfits."""
    print("\n🔍 Testing Trending Outfits...")
    response = requests.get(
        f"{BASE_URL}/recommendation/trending",
        headers=get_headers()
    )
    log_response(response, "Trending Outfits")
    assert response.status_code == 200


def test_refresh_token():
    """Test token refresh."""
    global access_token
    
    print("\n🔍 Testing Token Refresh...")
    data = {"refresh_token": refresh_token}
    response = requests.post(
        f"{BASE_URL}/auth/refresh",
        json=data,
        headers=get_headers()
    )
    log_response(response, "Refresh Token")
    assert response.status_code == 200
    
    result = response.json()
    access_token = result["access_token"]
    print(f"✓ Got new access token: {access_token[:20]}...")


def test_api_info():
    """Test API info."""
    print("\n🔍 Testing API Info...")
    response = requests.get(f"{BASE_URL}/api/v1/info")
    log_response(response, "API Info")
    assert response.status_code == 200


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("FASHION VIRTUAL TRY-ON API - Test Suite")
    print("="*60)
    
    try:
        # Connection test
        try:
            requests.get(f"{BASE_URL}/health")
            print("✓ Server is running")
        except requests.exceptions.ConnectionError:
            print("✗ Cannot connect to server")
            print(f"  Make sure server is running at {BASE_URL}")
            return
        
        # Run tests
        test_health()
        test_api_info()
        test_register()
        test_login()
        test_get_current_user()
        test_list_products()
        test_get_trending()
        test_refresh_token()
        test_create_product()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
