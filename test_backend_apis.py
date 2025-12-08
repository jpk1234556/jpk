import requests
import json

# Base URL for the Django API
BASE_URL = 'http://127.0.0.1:8000'

def test_units_api(auth_token):
    """Test Units CRUD API"""
    print("Testing Units API...")
    
    # Set headers
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }
    
    # Test GET all units
    response = requests.get(f'{BASE_URL}/api/units/', headers=headers)
    print(f"GET /api/units/ - Status: {response.status_code}")
    if response.status_code == 200:
        units = response.json()
        print(f"Found {len(units)} units")
        if units:
            unit_id = units[0]['id']
            # Test GET specific unit
            response = requests.get(f'{BASE_URL}/api/units/{unit_id}/', headers=headers)
            print(f"GET /api/units/{unit_id}/ - Status: {response.status_code}")
    
    print("-" * 40)

def test_tenants_api(auth_token):
    """Test Tenants CRUD API"""
    print("Testing Tenants API...")
    
    # Set headers
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }
    
    # Test GET all tenants
    response = requests.get(f'{BASE_URL}/api/tenants/', headers=headers)
    print(f"GET /api/tenants/ - Status: {response.status_code}")
    if response.status_code == 200:
        tenants = response.json()
        print(f"Found {len(tenants)} tenants")
        if tenants:
            tenant_id = tenants[0]['id']
            # Test GET specific tenant
            response = requests.get(f'{BASE_URL}/api/tenants/{tenant_id}/', headers=headers)
            print(f"GET /api/tenants/{tenant_id}/ - Status: {response.status_code}")
    
    print("-" * 40)

def test_payments_api(auth_token):
    """Test Payments CRUD API"""
    print("Testing Payments API...")
    
    # Set headers
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }
    
    # Test GET all payments
    response = requests.get(f'{BASE_URL}/api/payments/', headers=headers)
    print(f"GET /api/payments/ - Status: {response.status_code}")
    if response.status_code == 200:
        payments = response.json()
        print(f"Found {len(payments)} payments")
        if payments:
            payment_id = payments[0]['id']
            # Test GET specific payment
            response = requests.get(f'{BASE_URL}/api/payments/{payment_id}/', headers=headers)
            print(f"GET /api/payments/{payment_id}/ - Status: {response.status_code}")
    
    print("-" * 40)

def test_maintenance_api(auth_token):
    """Test Maintenance Requests CRUD API"""
    print("Testing Maintenance Requests API...")
    
    # Set headers
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }
    
    # Test GET all maintenance requests
    response = requests.get(f'{BASE_URL}/api/maintenance/', headers=headers)
    print(f"GET /api/maintenance/ - Status: {response.status_code}")
    if response.status_code == 200:
        requests_data = response.json()
        print(f"Found {len(requests_data)} maintenance requests")
        if requests_data:
            request_id = requests_data[0]['id']
            # Test GET specific maintenance request
            response = requests.get(f'{BASE_URL}/api/maintenance/{request_id}/', headers=headers)
            print(f"GET /api/maintenance/{request_id}/ - Status: {response.status_code}")
    
    print("-" * 40)

def test_login():
    """Test user login to get auth token"""
    print("Testing User Login...")
    
    # Test data (you'll need to adjust this based on your actual users)
    login_data = {
        'username': 'admin',
        'password': 'admin'
    }
    
    response = requests.post(f'{BASE_URL}/api/users/login/', data=login_data)
    print(f"POST /api/users/login/ - Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        auth_token = data['token']
        print(f"Login successful. Token: {auth_token[:10]}...")
        return auth_token
    else:
        print(f"Login failed: {response.text}")
        return None

def main():
    print("Backend API Testing Script")
    print("=" * 40)
    
    # Test login to get auth token
    auth_token = test_login()
    
    if auth_token:
        # Test all APIs
        test_units_api(auth_token)
        test_tenants_api(auth_token)
        test_payments_api(auth_token)
        test_maintenance_api(auth_token)
    else:
        print("Cannot proceed with API tests without authentication token")

if __name__ == '__main__':
    main()