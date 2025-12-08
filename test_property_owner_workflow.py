"""
User acceptance testing for property owner roles
"""
import requests
import json
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

# Test data
PROPERTY_OWNER_CREDENTIALS = {
    "username": "owner1",
    "password": "owner1"
}

NEW_UNIT_DATA = {
    "unit_number": "101",
    "type": "Apartment",
    "capacity": 4,
    "price": 1200.00,
    "status": "available"
}

NEW_TENANT_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "lease_start": "2025-12-01",
    "lease_end": "2026-11-30",
    "rent_amount": 1200.00,
    "deposit_amount": 2400.00
}

NEW_PAYMENT_DATA = {
    "amount": 1200.00,
    "payment_date": "2025-12-08",
    "payment_method": "bank_transfer",
    "description": "December rent payment"
}

NEW_MAINTENANCE_REQUEST_DATA = {
    "title": "Leaky Faucet",
    "description": "Kitchen faucet is leaking and needs repair",
    "priority": "medium",
    "status": "pending"
}

class PropertyOwnerWorkflowTester:
    def __init__(self):
        self.owner_token = None
        self.property_id = None
        self.unit_id = None
        self.tenant_id = None
        self.maintenance_request_id = None
    
    def test_property_owner_login(self):
        """Test property owner login functionality"""
        print("Testing property owner login...")
        response = requests.post(
            f"{BASE_URL}/api/users/login/",
            json=PROPERTY_OWNER_CREDENTIALS
        )
        
        if response.status_code == 200:
            data = response.json()
            self.owner_token = data['token']
            print("✓ Property owner login successful")
            return True
        else:
            print(f"✗ Property owner login failed: {response.status_code} - {response.text}")
            return False
    
    def test_get_owned_properties(self):
        """Test getting properties owned by the user"""
        print("Testing property retrieval...")
        if not self.owner_token:
            print("✗ Cannot get properties - missing owner token")
            return False
            
        response = requests.get(
            f"{BASE_URL}/api/properties/",
            headers={"Authorization": f"Token {self.owner_token}"}
        )
        
        if response.status_code == 200:
            properties = response.json()
            if properties:
                self.property_id = properties[0]['id']
                print(f"✓ Property retrieval successful - found {len(properties)} properties")
            else:
                print("⚠ No properties found for this owner")
            return True
        else:
            print(f"✗ Property retrieval failed: {response.status_code} - {response.text}")
            return False
    
    def test_create_unit(self):
        """Test creating a unit"""
        print("Testing unit creation...")
        if not self.owner_token or not self.property_id:
            print("✗ Cannot create unit - missing token or property ID")
            return False
            
        unit_data = NEW_UNIT_DATA.copy()
        unit_data['property'] = self.property_id
        
        response = requests.post(
            f"{BASE_URL}/api/units/",
            headers={"Authorization": f"Token {self.owner_token}"},
            json=unit_data
        )
        
        if response.status_code == 201:
            data = response.json()
            self.unit_id = data['id']
            print("✓ Unit creation successful")
            return True
        else:
            print(f"✗ Unit creation failed: {response.status_code} - {response.text}")
            return False
    
    def test_create_tenant(self):
        """Test creating a tenant"""
        print("Testing tenant creation...")
        if not self.owner_token or not self.unit_id:
            print("✗ Cannot create tenant - missing token or unit ID")
            return False
            
        tenant_data = NEW_TENANT_DATA.copy()
        tenant_data['unit'] = self.unit_id
        
        response = requests.post(
            f"{BASE_URL}/api/tenants/",
            headers={"Authorization": f"Token {self.owner_token}"},
            json=tenant_data
        )
        
        if response.status_code == 201:
            data = response.json()
            self.tenant_id = data['id']
            print("✓ Tenant creation successful")
            return True
        else:
            print(f"✗ Tenant creation failed: {response.status_code} - {response.text}")
            return False
    
    def test_record_payment(self):
        """Test recording a payment"""
        print("Testing payment recording...")
        if not self.owner_token or not self.tenant_id:
            print("✗ Cannot record payment - missing token or tenant ID")
            return False
            
        payment_data = NEW_PAYMENT_DATA.copy()
        payment_data['tenant'] = self.tenant_id
        
        response = requests.post(
            f"{BASE_URL}/api/payments/",
            headers={"Authorization": f"Token {self.owner_token}"},
            json=payment_data
        )
        
        if response.status_code == 201:
            print("✓ Payment recording successful")
            return True
        else:
            print(f"✗ Payment recording failed: {response.status_code} - {response.text}")
            return False
    
    def test_submit_maintenance_request(self):
        """Test submitting a maintenance request"""
        print("Testing maintenance request submission...")
        if not self.owner_token or not self.unit_id:
            print("✗ Cannot submit maintenance request - missing token or unit ID")
            return False
            
        maintenance_data = NEW_MAINTENANCE_REQUEST_DATA.copy()
        maintenance_data['unit'] = self.unit_id
        maintenance_data['submitted_by'] = self.get_current_user_id()
        
        response = requests.post(
            f"{BASE_URL}/api/maintenance/",
            headers={"Authorization": f"Token {self.owner_token}"},
            json=maintenance_data
        )
        
        if response.status_code == 201:
            data = response.json()
            self.maintenance_request_id = data['id']
            print("✓ Maintenance request submission successful")
            return True
        else:
            print(f"✗ Maintenance request submission failed: {response.status_code} - {response.text}")
            return False
    
    def test_property_owner_reports(self):
        """Test property owner reports functionality"""
        print("Testing property owner reports...")
        if not self.owner_token:
            print("✗ Cannot access reports - missing owner token")
            return False
            
        response = requests.get(
            f"{BASE_URL}/api/property-owner-module/reports/?type=summary",
            headers={"Authorization": f"Token {self.owner_token}"}
        )
        
        if response.status_code == 200:
            print("✓ Property owner reports access successful")
            return True
        else:
            print(f"✗ Property owner reports access failed: {response.status_code} - {response.text}")
            return False
    
    def get_current_user_id(self):
        """Helper method to get current user ID"""
        if not self.owner_token:
            return None
            
        response = requests.get(
            f"{BASE_URL}/api/users/",
            headers={"Authorization": f"Token {self.owner_token}"}
        )
        
        if response.status_code == 200:
            users = response.json()
            for user in users:
                if user['username'] == PROPERTY_OWNER_CREDENTIALS['username']:
                    return user['id']
        return None
    
    def run_complete_workflow(self):
        """Run the complete property owner workflow test"""
        print("=" * 50)
        print("PROPERTY OWNER WORKFLOW END-TO-END TEST")
        print("=" * 50)
        
        tests = [
            self.test_property_owner_login,
            self.test_get_owned_properties,
            self.test_create_unit,
            self.test_create_tenant,
            self.test_record_payment,
            self.test_submit_maintenance_request,
            self.test_property_owner_reports
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
    tester = PropertyOwnerWorkflowTester()
    success = tester.run_complete_workflow()
    exit(0 if success else 1)