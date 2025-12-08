import requests
import json

# Base URL for the API
BASE_URL = 'http://127.0.0.1:8000'

def login(username, password):
    """Login and get authentication token"""
    url = f'{BASE_URL}/api/users/login/'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()['token']
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def get_users(token):
    """Get list of users"""
    url = f'{BASE_URL}/api/users/'
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get users: {response.status_code} - {response.text}")
        return None

def create_user(token, username, email, password, role):
    """Create a new user"""
    url = f'{BASE_URL}/api/users/'
    headers = {
        'Authorization': f'Token {token}'
    }
    data = {
        'username': username,
        'email': email,
        'password': password,
        'role': role
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Failed to create user: {response.status_code} - {response.text}")
        return None

# Example usage
if __name__ == '__main__':
    # Login as admin
    token = login('admin', 'admin')
    if token:
        print(f"Login successful. Token: {token}")
        
        # Get list of users
        users = get_users(token)
        if users is not None:
            print("Users:")
            print(json.dumps(users, indent=2))
        
        # Create a new property owner
        new_user = create_user(token, 'property_owner1', 'owner1@example.com', 'password123', 'property_owner')
        if new_user:
            print("New user created:")
            print(json.dumps(new_user, indent=2))
    else:
        print("Login failed")