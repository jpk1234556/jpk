"""
End-to-end testing for the complete admin workflow
"""
import requests
import json
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

# Test data
ADMIN_CREDENTIALS = {
    "username": "admin2",
    "password": "admin2"
}

PROPERTY_OWNER_CREDENTIALS = {
    "username": "owner1",
    "password": "owner1"
}

NEW_PROPERTY_OWNER_DATA = {
    "username": "new_owner",
    "email": "new_owner@example.com",
    "password": "new_owner_password"
}

NEW_PROPERTY_DATA = {
    "name": "Test Property",
    "type": "apartment",
    "address": "123 Test Street, Test City"
}

class AdminWorkflowTester:
    def __init__(self):
        self.admin_token = None
        self.owner_token = None
        self.new_owner_id = None
        self.property_id = None
    
    def test_admin_login(self):
        """Test admin login functionality"""
        print("Testing admin login...")
        response = requests.post(
            f"{BASE_URL}/api/users/login/",
            json=ADMIN_CREDENTIALS
        )
        
        if response.status_code == 200:
            data = response.json()
            self.admin_token = data['token']
            print("✓ Admin login successful")
            return True
        else:
            print(f"✗ Admin login failed: {response.status_code} - {response.text}")
            return False
    
    def test_property_owner_registration(self):
        """Test property owner registration"""
        print("Testing property owner registration...")
        response = requests.post(
            f"{BASE_URL}/api/users/",
            json=NEW_PROPERTY_OWNER_DATA
        )
        
        if response.status_code == 201:
            data = response.json()
            self.new_owner_id = data['id']
            print("✓ Property owner registration successful")
            return True
        else:
            print(f"✗ Property owner registration failed: {response.status_code} - {response.text}")
            return False
    
    def test_approve_property_owner(self):
        """Test approving a property owner"""
        print("Testing property owner approval...")
        if not self.admin_token or not self.new_owner_id:
            print("✗ Cannot approve owner - missing token or owner ID")
            return False
            
        # Set the role to property_owner and approve
        response = requests.patch(
            f"{BASE_URL}/api/users/{self.new_owner_id}/",
            headers={"Authorization": f"Token {self.admin_token}"},
            json={
                "role": "property_owner",
                "is_approved": True
            }
        )
        
        if response.status_code == 200:
            print("✓ Property owner approval successful")
            return True
        else:
            print(f"✗ Property owner approval failed: {response.status_code} - {response.text}")
            return False
    
    def test_create_property(self):
        """Test creating a property"""
        print("Testing property creation...")
        if not self.admin_token:
            print("✗ Cannot create property - missing admin token")
            return False
            
        # First get the new owner's ID
        response = requests.get(
            f"{BASE_URL}/api/users/",
            headers={"Authorization": f"Token {self.admin_token}"}
        )
        
        if response.status_code != 200:
            print(f"✗ Failed to get users: {response.status_code}")
            return False
            
        users = response.json()
        owner_id = None
        for user in users:
            if user['username'] == NEW_PROPERTY_OWNER_DATA['username']:
                owner_id = user['id']
                break
                
        if not owner_id:
            print("✗ Could not find newly created owner")
            return False
            
        # Create property with owner
        property_data = NEW_PROPERTY_DATA.copy()
        property_data['owner'] = owner_id
        
        response = requests.post(
            f"{BASE_URL}/api/properties/",
            headers={"Authorization": f"Token {self.admin_token}"},
            json=property_data
        )
        
        if response.status_code == 201:
            data = response.json()
            self.property_id = data['id']
            print("✓ Property creation successful")
            return True
        else:
            print(f"✗ Property creation failed: {response.status_code} - {response.text}")
            return False
    
    def test_admin_reports(self):
        """Test admin reports functionality"""
        print("Testing admin reports...")
        if not self.admin_token:
            print("✗ Cannot access reports - missing admin token")
            return False
            
        response = requests.get(
            f"{BASE_URL}/api/admin-module/reports/?type=summary",
            headers={"Authorization": f"Token {self.admin_token}"}
        )
        
        if response.status_code == 200:
            print("✓ Admin reports access successful")
            return True
        else:
            print(f"✗ Admin reports access failed: {response.status_code} - {response.text}")
            return False
    
    def test_admin_settings(self):
        """Test admin settings functionality"""
        print("Testing admin settings...")
        if not self.admin_token:
            print("✗ Cannot access settings - missing admin token")
            return False
            
        # Get current settings
        response = requests.get(
            f"{BASE_URL}/api/admin-module/settings/",
            headers={"Authorization": f"Token {self.admin_token}"}
        )
        
        if response.status_code != 200:
            print(f"✗ Failed to get settings: {response.status_code} - {response.text}")
            return False
            
        # Update settings
        update_data = {
            "company_info": {
                "name": "Updated Property Management Inc.",
                "address": "456 Updated Street, Updated City, State 67890",
                "phone": "(555) 987-6543",
                "email": "updated@propertymanagement.com"
            }
        }
        
        response = requests.patch(
            f"{BASE_URL}/api/admin-module/settings/",
            headers={"Authorization": f"Token {self.admin_token}"},
            json=update_data
        )
        
        if response.status_code == 200:
            print("✓ Admin settings update successful")
            return True
        else:
            print(f"✗ Admin settings update failed: {response.status_code} - {response.text}")
            return False
    
    def run_complete_workflow(self):
        """Run the complete admin workflow test"""
        print("=" * 50)
        print("ADMIN WORKFLOW END-TO-END TEST")
        print("=" * 50)
        
        tests = [
            self.test_admin_login,
            self.test_property_owner_registration,
            self.test_approve_property_owner,
            self.test_create_property,
            self.test_admin_reports,
            self.test_admin_settings
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    print(f"Test {test.__name__} failed")
            except Exception as e:
                print(f"✗ Test {test.__name__} encountered an error: {str(e)}")
            time.sleep(1)  # Small delay between tests
        
        print("\n" + "=" * 50)
        print(f"TEST RESULTS: {passed}/{total} tests passed")
        print("=" * 50)
        
        return passed == total

if __name__ == "__main__":
    tester = AdminWorkflowTester()
    success = tester.run_complete_workflow()
    exit(0 if success else 1)