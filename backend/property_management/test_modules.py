import requests
import json

# Test the new module organization

def test_admin_endpoint():
    """Test the admin module dashboard endpoint"""
    print("Testing Admin Module Dashboard Endpoint...")
    
    # First, login to get a token
    login_data = {
        'username': 'admin',
        'password': 'admin'
    }
    
    login_response = requests.post('http://127.0.0.1:8000/api/users/login/', data=login_data)
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        print(f"Login successful. Token: {token[:10]}...")
        
        # Test the admin dashboard endpoint
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get('http://127.0.0.1:8000/api/admin-module/dashboard-stats/', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("Admin Dashboard Data:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"Error accessing admin dashboard: {response.status_code}")
            print(response.text)
            return False
    else:
        print("Login failed")
        print(login_response.text)
        return False

def test_property_owner_endpoint():
    """Test the property owner module dashboard endpoint"""
    print("\nTesting Property Owner Module Dashboard Endpoint...")
    
    # First, login to get a token
    login_data = {
        'username': 'admin',
        'password': 'admin'
    }
    
    login_response = requests.post('http://127.0.0.1:8000/api/users/login/', data=login_data)
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        print(f"Login successful. Token: {token[:10]}...")
        
        # Test the property owner dashboard endpoint
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get('http://127.0.0.1:8000/api/property-owner-module/dashboard-stats/', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("Property Owner Dashboard Data:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"Error accessing property owner dashboard: {response.status_code}")
            print(response.text)
            return False
    else:
        print("Login failed")
        print(login_response.text)
        return False

if __name__ == '__main__':
    print("Testing Backend Module Organization")
    print("=" * 40)
    
    admin_success = test_admin_endpoint()
    owner_success = test_property_owner_endpoint()
    
    print("\n" + "=" * 40)
    if admin_success and owner_success:
        print("✅ All tests passed! Module organization is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above for details.")