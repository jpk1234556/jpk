import requests
import json

def test_registration():
    """Test the property owner registration feature"""
    print("Testing Property Owner Registration...")
    
    # Test data
    registration_data = {
        'username': 'test_owner',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    
    # Send registration request
    response = requests.post(
        'http://127.0.0.1:8000/api/users/',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(registration_data)
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print("✅ Registration successful!")
        print(f"User ID: {data['id']}")
        print(f"Username: {data['username']}")
        print(f"Email: {data['email']}")
        print(f"Role: {data['role']}")
        print(f"Approved: {data['is_approved']}")
        return True
    else:
        print("❌ Registration failed!")
        print(f"Response: {response.text}")
        return False

def test_login_unapproved():
    """Test that unapproved users cannot log in"""
    print("\nTesting Login with Unapproved Account...")
    
    # Login data
    login_data = {
        'username': 'test_owner',
        'password': 'testpassword123'
    }
    
    # Send login request
    response = requests.post(
        'http://127.0.0.1:8000/api/users/login/',
        data=login_data
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 403:
        data = response.json()
        print("✅ Login correctly blocked for unapproved user!")
        print(f"Error: {data['error']}")
        return True
    else:
        print("❌ Login test failed!")
        print(f"Response: {response.text}")
        return False

if __name__ == '__main__':
    print("Property Owner Registration Feature Test")
    print("=" * 40)
    
    registration_success = test_registration()
    login_blocked = test_login_unapproved()
    
    print("\n" + "=" * 40)
    if registration_success and login_blocked:
        print("✅ All tests passed! Registration feature is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above for details.")