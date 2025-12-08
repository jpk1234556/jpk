import requests
import json

# Base URL for the Django API
BASE_URL = 'http://127.0.0.1:8000'

def test_frontend_backend_integration():
    """Test the integration between frontend and backend APIs"""
    print("Testing Frontend-Backend Integration...")
    print("=" * 50)
    
    # Test data
    login_data = {
        'username': 'admin',
        'password': 'admin'
    }
    
    # Login to get auth token
    print("1. Testing User Login...")
    response = requests.post(f'{BASE_URL}/api/users/login/', data=login_data)
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    data = response.json()
    auth_token = data['token']
    user = data['user']
    print(f"✅ Login successful. User: {user['username']}, Role: {user['role']}")
    
    # Set headers for authenticated requests
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }
    
    # Test Units API
    print("\n2. Testing Units API...")
    response = requests.get(f'{BASE_URL}/api/units/', headers=headers)
    if response.status_code == 200:
        units = response.json()
        print(f"✅ Units API working. Found {len(units)} units")
    else:
        print(f"❌ Units API failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Test Tenants API
    print("\n3. Testing Tenants API...")
    response = requests.get(f'{BASE_URL}/api/tenants/', headers=headers)
    if response.status_code == 200:
        tenants = response.json()
        print(f"✅ Tenants API working. Found {len(tenants)} tenants")
    else:
        print(f"❌ Tenants API failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Test Payments API
    print("\n4. Testing Payments API...")
    response = requests.get(f'{BASE_URL}/api/payments/', headers=headers)
    if response.status_code == 200:
        payments = response.json()
        print(f"✅ Payments API working. Found {len(payments)} payments")
    else:
        print(f"❌ Payments API failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Test Maintenance Requests API
    print("\n5. Testing Maintenance Requests API...")
    response = requests.get(f'{BASE_URL}/api/maintenance/', headers=headers)
    if response.status_code == 200:
        maintenance_requests = response.json()
        print(f"✅ Maintenance Requests API working. Found {len(maintenance_requests)} requests")
    else:
        print(f"❌ Maintenance Requests API failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All Frontend-Backend Integrations Working Successfully!")
    print("The frontend pages can now be connected to these real APIs.")
    return True

def main():
    print("Frontend-Backend Integration Test")
    print("=" * 50)
    
    try:
        success = test_frontend_backend_integration()
        if success:
            print("\n🎉 Integration test completed successfully!")
            print("All frontend pages can now use real data from the backend APIs.")
        else:
            print("\n❌ Integration test failed!")
            print("Please check the error messages above.")
    except Exception as e:
        print(f"\n❌ Integration test failed with exception: {e}")

if __name__ == '__main__':
    main()