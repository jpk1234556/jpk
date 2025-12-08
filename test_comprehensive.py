"""
Comprehensive testing including setup, execution, and cleanup
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

NEW_TEST_PROPERTY = {
    "name": "Test Property for Integration",
    "type": "apartment",
    "address": "123 Integration Test St, Test City"
}

NEW_TEST_UNIT = {
    "unit_number": "101",
    "type": "Apartment",
    "capacity": 2,
    "price": 1000.00,
    "status": "available"
}

NEW_TEST_TENANT = {
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com",
    "phone": "+1987654321",
    "lease_start": "2025-12-01",
    "lease_end": "2026-11-30",
    "rent_amount": 1000.00,
    "deposit_amount": 2000.00
}

class ComprehensiveTester:
    def __init__(self):
        self.admin_token = None
        self.owner_token = None
        self.owner_id = None
        self.property_id = None
        self.unit_id = None
        self.tenant_id = None
    
    def login_admin(self):
        """Login as admin"""
        print("Logging in as admin...")
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
            print(f"✗ Admin login failed: {response.status_code}")
            return False
    
    def login_owner(self):
        """Login as property owner"""
        print("Logging in as property owner...")
        response = requests.post(
            f"{BASE_URL}/api/users/login/",
            json=PROPERTY_OWNER_CREDENTIALS
        )
        
        if response.status_code == 200:
            data = response.json()
            self.owner_token = data['token']
            self.owner_id = data['user']['id']
            print("✓ Property owner login successful")
            return True
        else:
            print(f"✗ Property owner login failed: {response.status_code}")
            return False
    
    def setup_test_property(self):
        """Create a test property for the owner"""
        print("Setting up test property...")
        if not self.admin_token or not self.owner_id:
            print("✗ Cannot create property - missing admin token or owner ID")
            return False
        
        # Create property with owner
        property_data = NEW_TEST_PROPERTY.copy()
        property_data['owner'] = self.owner_id
        
        response = requests.post(
            f"{BASE_URL}/api/properties/",
            headers={"Authorization": f"Token {self.admin_token}"},
            json=property_data
        )
        
        if response.status_code == 201:
            data = response.json()
            self.property_id = data['id']
            print("✓ Test property creation successful")
            return True
        else:
            print(f"✗ Test property creation failed: {response.status_code} - {response.text}")
            return False
    
    def test_owner_can_see_property(self):
        """Verify owner can see their property"""
        print("Testing property visibility for owner...")
        if not self.owner_token:
            print("✗ Cannot test property visibility - missing owner token")
            return False
            
        response = requests.get(
            f"{BASE_URL}/api/properties/",
            headers={"Authorization": f"Token {self.owner_token}"}
        )
        
        if response.status_code == 200:
            properties = response.json()
            if len(properties) > 0:
                print(f"✓ Owner can see {len(properties)} properties")
                return True
            else:
                print("⚠ Owner cannot see any properties")
                return False
        else:
            print(f"✗ Property retrieval failed: {response.status_code}")
            return False
    
    def test_create_unit(self):
        """Test creating a unit"""
        print("Testing unit creation...")
        if not self.owner_token or not self.property_id:
            print("✗ Cannot create unit - missing token or property ID")
            return False
            
        unit_data = NEW_TEST_UNIT.copy()
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
            
        tenant_data = NEW_TEST_TENANT.copy()
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
    
    def test_crud_operations(self):
        """Test all CRUD operations"""
        print("Testing CRUD operations...")
        
        # Test creating payment
        if self.tenant_id and self.owner_token:
            payment_data = {
                "tenant": self.tenant_id,
                "amount": 1000.00,
                "payment_date": "2025-12-08",
                "payment_method": "bank_transfer"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/payments/",
                headers={"Authorization": f"Token {self.owner_token}"},
                json=payment_data
            )
            
            if response.status_code == 201:
                print("✓ Payment creation successful")
            else:
                print(f"✗ Payment creation failed: {response.status_code}")
        
        # Test creating maintenance request
        if self.unit_id and self.owner_token:
            maintenance_data = {
                "unit": self.unit_id,
                "submitted_by": self.owner_id,
                "title": "Test Maintenance Request",
                "description": "This is a test maintenance request",
                "priority": "medium",
                "status": "pending"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/maintenance/",
                headers={"Authorization": f"Token {self.owner_token}"},
                json=maintenance_data
            )
            
            if response.status_code == 201:
                print("✓ Maintenance request creation successful")
            else:
                print(f"✗ Maintenance request creation failed: {response.status_code}")
        
        return True
    
    def test_reports_and_dashboard(self):
        """Test reports and dashboard functionality"""
        print("Testing reports and dashboard...")
        
        # Test admin reports
        if self.admin_token:
            response = requests.get(
                f"{BASE_URL}/api/admin-module/reports/?type=summary",
                headers={"Authorization": f"Token {self.admin_token}"}
            )
            
            if response.status_code == 200:
                print("✓ Admin reports access successful")
            else:
                print(f"✗ Admin reports access failed: {response.status_code}")
        
        # Test owner reports
        if self.owner_token:
            response = requests.get(
                f"{BASE_URL}/api/property-owner-module/reports/?type=summary",
                headers={"Authorization": f"Token {self.owner_token}"}
            )
            
            if response.status_code == 200:
                print("✓ Property owner reports access successful")
            else:
                print(f"✗ Property owner reports access failed: {response.status_code}")
        
        # Test dashboards
        if self.admin_token:
            response = requests.get(
                f"{BASE_URL}/api/admin-module/dashboard-stats/",
                headers={"Authorization": f"Token {self.admin_token}"}
            )
            
            if response.status_code == 200:
                print("✓ Admin dashboard access successful")
            else:
                print(f"✗ Admin dashboard access failed: {response.status_code}")
        
        if self.owner_token:
            response = requests.get(
                f"{BASE_URL}/api/property-owner-module/dashboard-stats/",
                headers={"Authorization": f"Token {self.owner_token}"}
            )
            
            if response.status_code == 200:
                print("✓ Property owner dashboard access successful")
            else:
                print(f"✗ Property owner dashboard access failed: {response.status_code}")
        
        return True
    
    def run_comprehensive_test(self):
        """Run the complete comprehensive test"""
        print("=" * 60)
        print("COMPREHENSIVE END-TO-END TESTING")
        print("=" * 60)
        
        # Step 1: Authentication
        if not self.login_admin() or not self.login_owner():
            print("✗ Authentication failed")
            return False
        
        # Step 2: Setup
        if not self.setup_test_property():
            print("✗ Test setup failed")
            return False
        
        # Small delay to ensure data propagation
        time.sleep(1)
        
        # Step 3: Core functionality tests
        tests = [
            self.test_owner_can_see_property,
            self.test_create_unit,
            self.test_create_tenant,
            self.test_crud_operations,
            self.test_reports_and_dashboard
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                print()  # Add spacing
            except Exception as e:
                print(f"✗ Test {test.__name__} encountered an error: {str(e)}")
            time.sleep(0.5)  # Small delay between tests
        
        print("=" * 60)
        print(f"COMPREHENSIVE TEST RESULTS: {passed}/{total} test groups passed")
        print("=" * 60)
        
        if passed == total:
            print("🎉 All comprehensive tests passed!")
            print("The system is working correctly end-to-end.")
        else:
            print("⚠ Some tests failed. Please review the results above.")
        
        return passed == total

if __name__ == "__main__":
    tester = ComprehensiveTester()
    success = tester.run_comprehensive_test()
    exit(0 if success else 1)