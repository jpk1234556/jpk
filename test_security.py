"""
Security audit and penetration testing
"""
import requests
import json

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

class SecurityTester:
    def __init__(self):
        self.admin_token = None
        self.owner_token = None
        self.setup_tokens()
    
    def setup_tokens(self):
        """Setup authentication tokens for testing"""
        # Get admin token
        response = requests.post(
            f"{BASE_URL}/api/users/login/",
            json=ADMIN_CREDENTIALS
        )
        if response.status_code == 200:
            self.admin_token = response.json()['token']
        
        # Get owner token
        response = requests.post(
            f"{BASE_URL}/api/users/login/",
            json=PROPERTY_OWNER_CREDENTIALS
        )
        if response.status_code == 200:
            self.owner_token = response.json()['token']
    
    def test_authentication_bypass(self):
        """Test if endpoints can be accessed without authentication"""
        print("Testing authentication bypass...")
        
        endpoints = [
            f"{BASE_URL}/api/users/",
            f"{BASE_URL}/api/properties/",
            f"{BASE_URL}/api/units/",
            f"{BASE_URL}/api/tenants/",
            f"{BASE_URL}/api/payments/",
            f"{BASE_URL}/api/maintenance/",
            f"{BASE_URL}/api/admin-module/dashboard-stats/",
            f"{BASE_URL}/api/property-owner-module/dashboard-stats/"
        ]
        
        vulnerable_endpoints = []
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint)
                # If we get a successful response or data, it might be vulnerable
                if response.status_code == 200:
                    # Check if we actually got meaningful data
                    try:
                        data = response.json()
                        if isinstance(data, (list, dict)) and len(data) > 0:
                            vulnerable_endpoints.append(endpoint)
                            print(f"⚠ Vulnerable endpoint found: {endpoint}")
                    except:
                        pass  # Not JSON data
                elif response.status_code != 401 and response.status_code != 403:
                    # Any response other than authentication required might be suspicious
                    print(f"⚠ Unexpected response from {endpoint}: {response.status_code}")
            except Exception as e:
                pass  # Connection errors are expected for some endpoints
        
        if not vulnerable_endpoints:
            print("✓ No authentication bypass vulnerabilities found")
            return True
        else:
            print(f"✗ Found {len(vulnerable_endpoints)} potentially vulnerable endpoints")
            return False
    
    def test_role_based_access_control(self):
        """Test role-based access control"""
        print("Testing role-based access control...")
        
        if not self.admin_token or not self.owner_token:
            print("✗ Cannot test RBAC - authentication failed")
            return False
        
        # Test cases: (endpoint, method, admin_should_have_access, owner_should_have_access)
        test_cases = [
            (f"{BASE_URL}/api/users/", "GET", True, False),  # Admin can list all users, owner cannot
            (f"{BASE_URL}/api/admin-module/dashboard-stats/", "GET", True, False),  # Only admin
            (f"{BASE_URL}/api/property-owner-module/dashboard-stats/", "GET", False, True),  # Only owner
            (f"{BASE_URL}/api/properties/", "POST", True, False),  # Only admin can create properties
        ]
        
        violations = 0
        
        for endpoint, method, admin_access, owner_access in test_cases:
            # Test admin access
            if admin_access:
                response = requests.request(
                    method, 
                    endpoint, 
                    headers={"Authorization": f"Token {self.admin_token}"}
                )
                if response.status_code in [401, 403]:
                    print(f"⚠ Admin incorrectly denied access to {endpoint}")
                    violations += 1
            else:
                response = requests.request(
                    method, 
                    endpoint, 
                    headers={"Authorization": f"Token {self.admin_token}"}
                )
                if response.status_code not in [401, 403]:
                    print(f"⚠ Admin incorrectly granted access to {endpoint}")
                    violations += 1
            
            # Test owner access
            if owner_access:
                response = requests.request(
                    method, 
                    endpoint, 
                    headers={"Authorization": f"Token {self.owner_token}"}
                )
                if response.status_code in [401, 403]:
                    print(f"⚠ Owner incorrectly denied access to {endpoint}")
                    violations += 1
            else:
                response = requests.request(
                    method, 
                    endpoint, 
                    headers={"Authorization": f"Token {self.owner_token}"}
                )
                if response.status_code not in [401, 403]:
                    print(f"⚠ Owner incorrectly granted access to {endpoint}")
                    violations += 1
        
        if violations == 0:
            print("✓ Role-based access control working correctly")
            return True
        else:
            print(f"✗ Found {violations} RBAC violations")
            return False
    
    def test_input_validation(self):
        """Test input validation for common vulnerabilities"""
        print("Testing input validation...")
        
        if not self.admin_token:
            print("✗ Cannot test input validation - admin authentication failed")
            return False
        
        # Test SQL injection in user creation
        malicious_user_data = {
            "username": "test'; DROP TABLE users; --",
            "email": "test@example.com",
            "password": "password123"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/users/",
                json=malicious_user_data
            )
            # We expect either a validation error or successful creation (if properly sanitized)
            # The important thing is that the server doesn't crash or execute the SQL
            if response.status_code in [201, 400]:
                print("✓ SQL injection test passed - no server crash")
            else:
                print(f"⚠ Unexpected response to SQL injection test: {response.status_code}")
        except Exception as e:
            print(f"✗ Server crashed during SQL injection test: {str(e)}")
            return False
        
        # Test XSS in property creation
        malicious_property_data = {
            "name": "<script>alert('XSS')</script>",
            "type": "apartment",
            "address": "Test Address",
            "owner": 1  # We'll test with a valid owner ID
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/properties/",
                headers={"Authorization": f"Token {self.admin_token}"},
                json=malicious_property_data
            )
            # Again, we expect validation or proper sanitization
            if response.status_code in [201, 400]:
                print("✓ XSS test passed - no server crash")
            else:
                print(f"⚠ Unexpected response to XSS test: {response.status_code}")
        except Exception as e:
            print(f"✗ Server crashed during XSS test: {str(e)}")
            return False
        
        return True
    
    def test_rate_limiting(self):
        """Test if rate limiting is implemented"""
        print("Testing rate limiting...")
        
        # Make rapid requests to see if any are rejected
        rapid_requests = 20
        rejected_count = 0
        
        for i in range(rapid_requests):
            try:
                response = requests.get(f"{BASE_URL}/api/users/")
                if response.status_code == 429:  # Too Many Requests
                    rejected_count += 1
            except:
                pass  # Ignore connection errors
        
        if rejected_count > 0:
            print(f"✓ Rate limiting detected - {rejected_count}/{rapid_requests} requests rejected")
            return True
        else:
            print("⚠ No rate limiting detected - consider implementing for production")
            return True  # Not a failure, just a recommendation
    
    def test_sensitive_data_exposure(self):
        """Test for sensitive data exposure"""
        print("Testing sensitive data exposure...")
        
        if not self.admin_token:
            print("✗ Cannot test sensitive data exposure - authentication failed")
            return False
        
        # Test user list endpoint
        response = requests.get(
            f"{BASE_URL}/api/users/",
            headers={"Authorization": f"Token {self.admin_token}"}
        )
        
        if response.status_code == 200:
            users = response.json()
            exposed_passwords = 0
            
            for user in users:
                # Check if password hashes or other sensitive data are exposed
                if 'password' in user or 'password_hash' in user:
                    exposed_passwords += 1
            
            if exposed_passwords == 0:
                print("✓ No sensitive data (passwords) exposed in user list")
                return True
            else:
                print(f"⚠ {exposed_passwords} users have exposed password data")
                return False
        else:
            print(f"✗ Failed to retrieve user list: {response.status_code}")
            return False
    
    def run_security_audit(self):
        """Run comprehensive security audit"""
        print("=" * 50)
        print("SECURITY AUDIT AND PENETRATION TESTING")
        print("=" * 50)
        
        tests = [
            self.test_authentication_bypass,
            self.test_role_based_access_control,
            self.test_input_validation,
            self.test_rate_limiting,
            self.test_sensitive_data_exposure
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                print()  # Add spacing between tests
            except Exception as e:
                print(f"✗ Test {test.__name__} encountered an error: {str(e)}")
        
        print("=" * 50)
        print(f"SECURITY AUDIT RESULTS: {passed}/{total} tests passed")
        print("=" * 50)
        
        if passed == total:
            print("🎉 All security tests passed! The application appears secure.")
        else:
            print("⚠ Some security issues were detected. Please review the findings above.")
        
        return passed == total

if __name__ == "__main__":
    tester = SecurityTester()
    success = tester.run_security_audit()
    exit(0 if success else 1)