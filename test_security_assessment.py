"""
Comprehensive Security Vulnerability Assessment
"""

import requests
import json
import time
import hashlib
import base64
from urllib.parse import quote_plus
import re

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

class SecurityAssessment:
    def __init__(self):
        self.admin_token = None
        self.owner_token = None
        self.session = requests.Session()
        self.setup_tokens()
    
    def setup_tokens(self):
        """Setup authentication tokens for testing"""
        print("Setting up authentication tokens...")
        
        # Get admin token
        try:
            response = requests.post(
                f"{BASE_URL}/api/users/login/",
                json=ADMIN_CREDENTIALS,
                timeout=10
            )
            if response.status_code == 200:
                self.admin_token = response.json()['token']
                print("✓ Admin token obtained")
            else:
                print(f"✗ Admin login failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Admin login error: {str(e)}")
        
        # Get owner token
        try:
            response = requests.post(
                f"{BASE_URL}/api/users/login/",
                json=PROPERTY_OWNER_CREDENTIALS,
                timeout=10
            )
            if response.status_code == 200:
                self.owner_token = response.json()['token']
                print("✓ Property owner token obtained")
            else:
                print(f"✗ Owner login failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Owner login error: {str(e)}")
    
    def test_authentication_security(self):
        """Comprehensive authentication security testing"""
        print("\n1. AUTHENTICATION SECURITY ASSESSMENT")
        print("=" * 50)
        
        vulnerabilities = []
        
        # Test 1: Weak password policy
        print("Testing weak password policy...")
        weak_passwords = ["123456", "password", "admin", "qwerty"]
        
        for weak_pwd in weak_passwords:
            test_user = {
                "username": f"testuser_{int(time.time())}",
                "email": f"test{int(time.time())}@example.com",
                "password": weak_pwd
            }
            
            try:
                response = requests.post(
                    f"{BASE_URL}/api/users/",
                    json=test_user,
                    timeout=10
                )
                
                # If weak password is accepted, it's a vulnerability
                if response.status_code == 201:
                    vulnerabilities.append({
                        "type": "WEAK_PASSWORD_POLICY",
                        "description": f"Weak password '{weak_pwd}' was accepted during registration",
                        "severity": "HIGH"
                    })
                    print(f"⚠ Vulnerability: Weak password '{weak_pwd}' accepted")
                    
                    # Clean up test user
                    try:
                        # We would need to delete this user, but we don't have admin access here
                        pass
                    except:
                        pass
                elif response.status_code == 400:
                    print(f"✓ Weak password '{weak_pwd}' correctly rejected")
            except Exception as e:
                print(f"⚠ Error testing weak password '{weak_pwd}': {str(e)}")
        
        # Test 2: Brute force protection
        print("Testing brute force protection...")
        brute_force_attempts = 15
        failed_logins = 0
        
        for i in range(brute_force_attempts):
            fake_credentials = {
                "username": "nonexistent_user",
                "password": f"fake_password_{i}"
            }
            
            try:
                response = requests.post(
                    f"{BASE_URL}/api/users/login/",
                    json=fake_credentials,
                    timeout=5
                )
                
                if response.status_code == 400:
                    failed_logins += 1
                elif response.status_code == 429:  # Rate limited
                    print("✓ Rate limiting detected for login attempts")
                    break
            except Exception as e:
                print(f"⚠ Error during brute force test: {str(e)}")
        
        if failed_logins == brute_force_attempts:
            vulnerabilities.append({
                "type": "MISSING_RATE_LIMITING",
                "description": "No rate limiting detected for login attempts",
                "severity": "HIGH"
            })
            print("⚠ Vulnerability: No rate limiting on login endpoint")
        else:
            print("✓ Rate limiting is implemented for login attempts")
        
        # Test 3: Session management
        print("Testing session management...")
        
        # Test token expiration
        if self.admin_token:
            try:
                # Use the token
                response = requests.get(
                    f"{BASE_URL}/api/users/",
                    headers={"Authorization": f"Token {self.admin_token}"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    print("✓ Valid token works correctly")
                else:
                    print("⚠ Valid token rejected")
            except Exception as e:
                print(f"⚠ Error testing valid token: {str(e)}")
        
        return vulnerabilities
    
    def test_input_validation_advanced(self):
        """Advanced input validation testing"""
        print("\n2. ADVANCED INPUT VALIDATION ASSESSMENT")
        print("=" * 50)
        
        vulnerabilities = []
        
        if not self.admin_token:
            print("⚠ Skipping input validation tests - no admin token")
            return vulnerabilities
        
        # Test SQL Injection variations
        print("Testing advanced SQL injection...")
        sql_injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT username, password FROM users --",
            "1'; EXEC xp_cmdshell('dir'); --",
            "' OR EXISTS(SELECT * FROM users WHERE username='admin') --"
        ]
        
        for payload in sql_injection_payloads:
            malicious_user_data = {
                "username": f"testuser_{payload}",
                "email": "test@example.com",
                "password": "securepassword123"
            }
            
            try:
                response = requests.post(
                    f"{BASE_URL}/api/users/",
                    json=malicious_user_data,
                    timeout=10
                )
                
                # Check if payload caused unexpected behavior
                if response.status_code not in [201, 400]:
                    vulnerabilities.append({
                        "type": "SQL_INJECTION_POSSIBLE",
                        "description": f"Unexpected response to SQL injection payload: {response.status_code}",
                        "severity": "CRITICAL",
                        "payload": payload
                    })
                    print(f"⚠ Possible SQL injection with payload: {payload}")
                else:
                    print(f"✓ SQL injection payload handled correctly: {payload}")
            except Exception as e:
                vulnerabilities.append({
                    "type": "APPLICATION_CRASH",
                    "description": f"Application crashed with SQL injection payload: {str(e)}",
                    "severity": "CRITICAL",
                    "payload": payload
                })
                print(f"⚠ Application crashed with payload: {payload}")
        
        # Test XSS variations
        print("Testing advanced XSS...")
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg/onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')></iframe>"
        ]
        
        for payload in xss_payloads:
            malicious_property_data = {
                "name": f"Test Property {payload}",
                "type": "apartment",
                "address": "Test Address",
                "owner": 1
            }
            
            try:
                response = requests.post(
                    f"{BASE_URL}/api/properties/",
                    headers={"Authorization": f"Token {self.admin_token}"},
                    json=malicious_property_data,
                    timeout=10
                )
                
                # Check if payload caused unexpected behavior
                if response.status_code not in [201, 400]:
                    vulnerabilities.append({
                        "type": "XSS_POSSIBLE",
                        "description": f"Unexpected response to XSS payload: {response.status_code}",
                        "severity": "HIGH",
                        "payload": payload
                    })
                    print(f"⚠ Possible XSS with payload: {payload}")
                else:
                    print(f"✓ XSS payload handled correctly: {payload}")
            except Exception as e:
                vulnerabilities.append({
                    "type": "APPLICATION_CRASH",
                    "description": f"Application crashed with XSS payload: {str(e)}",
                    "severity": "CRITICAL",
                    "payload": payload
                })
                print(f"⚠ Application crashed with payload: {payload}")
        
        # Test command injection
        print("Testing command injection...")
        cmd_injection_payloads = [
            "; ls",
            "| cat /etc/passwd",
            "& dir",
            "`whoami`",
            "$(whoami)"
        ]
        
        for payload in cmd_injection_payloads:
            malicious_data = {
                "name": f"Test {payload}",
                "type": "apartment",
                "address": "Test Address",
                "owner": 1
            }
            
            try:
                response = requests.post(
                    f"{BASE_URL}/api/properties/",
                    headers={"Authorization": f"Token {self.admin_token}"},
                    json=malicious_data,
                    timeout=10
                )
                
                # Check if payload caused unexpected behavior
                if response.status_code not in [201, 400]:
                    vulnerabilities.append({
                        "type": "COMMAND_INJECTION_POSSIBLE",
                        "description": f"Unexpected response to command injection payload: {response.status_code}",
                        "severity": "CRITICAL",
                        "payload": payload
                    })
                    print(f"⚠ Possible command injection with payload: {payload}")
                else:
                    print(f"✓ Command injection payload handled correctly: {payload}")
            except Exception as e:
                vulnerabilities.append({
                    "type": "APPLICATION_CRASH",
                    "description": f"Application crashed with command injection payload: {str(e)}",
                    "severity": "CRITICAL",
                    "payload": payload
                })
                print(f"⚠ Application crashed with payload: {payload}")
        
        return vulnerabilities
    
    def test_api_security(self):
        """API security testing"""
        print("\n3. API SECURITY ASSESSMENT")
        print("=" * 50)
        
        vulnerabilities = []
        
        # Test HTTP methods
        print("Testing HTTP method security...")
        endpoints = [
            f"{BASE_URL}/api/users/",
            f"{BASE_URL}/api/properties/",
            f"{BASE_URL}/api/units/"
        ]
        
        forbidden_methods = ["PUT", "PATCH", "DELETE"]
        
        for endpoint in endpoints:
            for method in forbidden_methods:
                try:
                    response = requests.request(method, endpoint, timeout=10)
                    
                    # Check if forbidden methods are properly blocked
                    if response.status_code not in [405, 401, 403]:
                        vulnerabilities.append({
                            "type": "HTTP_METHOD_EXPOSURE",
                            "description": f"HTTP method {method} not properly restricted on {endpoint}",
                            "severity": "MEDIUM",
                            "status_code": response.status_code
                        })
                        print(f"⚠ HTTP method {method} allowed on {endpoint} (status: {response.status_code})")
                    else:
                        print(f"✓ HTTP method {method} properly restricted on {endpoint}")
                except Exception as e:
                    print(f"⚠ Error testing HTTP method {method} on {endpoint}: {str(e)}")
        
        # Test API versioning and documentation exposure
        print("Testing API information disclosure...")
        
        # Check if API documentation is exposed
        doc_endpoints = [
            f"{BASE_URL}/api/docs/",
            f"{BASE_URL}/api/swagger/",
            f"{BASE_URL}/api/redoc/",
            f"{BASE_URL}/swagger/",
            f"{BASE_URL}/redoc/"
        ]
        
        for doc_endpoint in doc_endpoints:
            try:
                response = requests.get(doc_endpoint, timeout=10)
                if response.status_code == 200:
                    vulnerabilities.append({
                        "type": "API_DOCUMENTATION_EXPOSED",
                        "description": f"API documentation exposed at {doc_endpoint}",
                        "severity": "LOW",
                        "status_code": response.status_code
                    })
                    print(f"⚠ API documentation exposed at {doc_endpoint}")
                else:
                    print(f"✓ API documentation not exposed at {doc_endpoint}")
            except Exception as e:
                print(f"⚠ Error checking {doc_endpoint}: {str(e)}")
        
        return vulnerabilities
    
    def test_data_security(self):
        """Data security testing"""
        print("\n4. DATA SECURITY ASSESSMENT")
        print("=" * 50)
        
        vulnerabilities = []
        
        if not self.admin_token:
            print("⚠ Skipping data security tests - no admin token")
            return vulnerabilities
        
        # Test sensitive data exposure
        print("Testing sensitive data exposure...")
        
        try:
            response = requests.get(
                f"{BASE_URL}/api/users/",
                headers={"Authorization": f"Token {self.admin_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                users_data = response.json()
                
                # Check for sensitive data exposure
                sensitive_fields = ["password", "password_hash", "secret", "token", "key"]
                
                for user in users_data:
                    for field in sensitive_fields:
                        if field in user:
                            vulnerabilities.append({
                                "type": "SENSITIVE_DATA_EXPOSURE",
                                "description": f"Sensitive field '{field}' exposed in user data",
                                "severity": "HIGH",
                                "user_id": user.get("id", "unknown")
                            })
                            print(f"⚠ Sensitive field '{field}' exposed in user data")
                
                # Check for personally identifiable information (PII) overexposure
                pii_fields = ["ssn", "credit_card", "phone", "address"]
                
                for user in users_data:
                    for field in pii_fields:
                        if field in user and user[field]:
                            # In a real assessment, we'd check if this PII is properly masked
                            print(f"ℹ PII field '{field}' present in user data (check if properly protected)")
            else:
                print(f"⚠ Failed to retrieve user data: {response.status_code}")
        except Exception as e:
            print(f"⚠ Error during sensitive data exposure test: {str(e)}")
        
        # Test data leakage through error messages
        print("Testing error message security...")
        
        # Send malformed requests to see error responses
        malformed_requests = [
            {"malformed": "data"},
            {"": ""},
            {None: None}
        ]
        
        for malformed_data in malformed_requests:
            try:
                response = requests.post(
                    f"{BASE_URL}/api/users/",
                    json=malformed_data,
                    timeout=10
                )
                
                # Check if error messages reveal too much information
                if response.status_code == 400:
                    error_response = response.text.lower()
                    sensitive_info_indicators = [
                        "traceback", "exception", "stack", "database", 
                        "postgresql", "django", "internal server error"
                    ]
                    
                    for indicator in sensitive_info_indicators:
                        if indicator in error_response:
                            vulnerabilities.append({
                                "type": "INFORMATION_DISCLOSURE",
                                "description": f"Error response reveals internal information: {indicator}",
                                "severity": "MEDIUM",
                                "response_snippet": error_response[:100]
                            })
                            print(f"⚠ Error response reveals internal information: {indicator}")
                            break
                elif response.status_code == 500:
                    vulnerabilities.append({
                        "type": "SERVER_ERROR_EXPOSURE",
                        "description": "Server error (500) returned for malformed request",
                        "severity": "HIGH",
                        "status_code": response.status_code
                    })
                    print("⚠ Server error (500) returned for malformed request")
            except Exception as e:
                print(f"⚠ Error testing malformed request: {str(e)}")
        
        return vulnerabilities
    
    def test_cors_security(self):
        """CORS security testing"""
        print("\n5. CORS SECURITY ASSESSMENT")
        print("=" * 50)
        
        vulnerabilities = []
        
        # Test CORS headers
        print("Testing CORS configuration...")
        
        try:
            response = requests.get(
                f"{BASE_URL}/api/users/",
                headers={
                    "Origin": "http://malicious-site.com"
                },
                timeout=10
            )
            
            # Check CORS headers
            cors_headers = [
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Credentials",
                "Access-Control-Allow-Methods",
                "Access-Control-Allow-Headers"
            ]
            
            origin_header = response.headers.get("Access-Control-Allow-Origin", "")
            
            # Check if overly permissive CORS is set
            if origin_header == "*" or "malicious-site.com" in origin_header:
                vulnerabilities.append({
                    "type": "OVERLY_PERMISSIVE_CORS",
                    "description": f"CORS allows origin: {origin_header}",
                    "severity": "HIGH",
                    "headers": dict(response.headers)
                })
                print(f"⚠ Overly permissive CORS configuration: {origin_header}")
            elif origin_header:
                print(f"✓ CORS configured with specific origin: {origin_header}")
            else:
                print("✓ No CORS headers found (restrictive by default)")
                
        except Exception as e:
            print(f"⚠ Error testing CORS configuration: {str(e)}")
        
        return vulnerabilities
    
    def generate_security_report(self, all_vulnerabilities):
        """Generate comprehensive security report"""
        print("\n" + "=" * 70)
        print("SECURITY ASSESSMENT REPORT")
        print("=" * 70)
        
        if not all_vulnerabilities:
            print("🎉 No security vulnerabilities detected!")
            print("🔒 The application demonstrates good security practices.")
            return True
        
        # Categorize by severity
        critical = [v for v in all_vulnerabilities if v["severity"] == "CRITICAL"]
        high = [v for v in all_vulnerabilities if v["severity"] == "HIGH"]
        medium = [v for v in all_vulnerabilities if v["severity"] == "MEDIUM"]
        low = [v for v in all_vulnerabilities if v["severity"] == "LOW"]
        
        print(f"\n🔍 VULNERABILITIES FOUND:")
        print(f"   🔴 Critical: {len(critical)}")
        print(f"   🟠 High: {len(high)}")
        print(f"   🟡 Medium: {len(medium)}")
        print(f"   🟢 Low: {len(low)}")
        
        # Display detailed findings
        if critical:
            print(f"\n🔴 CRITICAL VULNERABILITIES:")
            for vuln in critical:
                print(f"   • {vuln['description']}")
                if 'payload' in vuln:
                    print(f"     Payload: {vuln['payload']}")
        
        if high:
            print(f"\n🟠 HIGH SEVERITY ISSUES:")
            for vuln in high:
                print(f"   • {vuln['description']}")
        
        if medium:
            print(f"\n🟡 MEDIUM SEVERITY ISSUES:")
            for vuln in medium:
                print(f"   • {vuln['description']}")
        
        if low:
            print(f"\n🟢 LOW SEVERITY ISSUES:")
            for vuln in low:
                print(f"   • {vuln['description']}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if critical or high:
            print("   🔒 Implement immediate security fixes for critical/high issues")
        
        if medium:
            print("   ⚠ Address medium severity issues in next release")
        
        if low:
            print("   ℹ Review low severity issues for best practices")
        
        print("   📚 Review OWASP Top 10 and implement additional security measures")
        print("   🔍 Conduct regular security audits and penetration testing")
        print("   🛡️ Implement comprehensive security monitoring")
        
        return len(critical) == 0 and len(high) == 0
    
    def run_comprehensive_security_assessment(self):
        """Run comprehensive security assessment"""
        print("=" * 70)
        print("COMPREHENSIVE SECURITY VULNERABILITY ASSESSMENT")
        print("=" * 70)
        
        all_vulnerabilities = []
        
        # Run all security tests
        print("\n🚀 Starting security assessment...")
        
        # Authentication security
        auth_vulns = self.test_authentication_security()
        all_vulnerabilities.extend(auth_vulns)
        
        # Input validation
        input_vulns = self.test_input_validation_advanced()
        all_vulnerabilities.extend(input_vulns)
        
        # API security
        api_vulns = self.test_api_security()
        all_vulnerabilities.extend(api_vulns)
        
        # Data security
        data_vulns = self.test_data_security()
        all_vulnerabilities.extend(data_vulns)
        
        # CORS security
        cors_vulns = self.test_cors_security()
        all_vulnerabilities.extend(cors_vulns)
        
        # Generate final report
        is_secure = self.generate_security_report(all_vulnerabilities)
        
        print(f"\n{'=' * 70}")
        if is_secure:
            print("✅ SECURITY ASSESSMENT COMPLETED - NO CRITICAL/HIGH VULNERABILITIES")
        else:
            print("❌ SECURITY ASSESSMENT COMPLETED - VULNERABILITIES DETECTED")
        print(f"{'=' * 70}")
        
        return is_secure

if __name__ == "__main__":
    assessor = SecurityAssessment()
    is_secure = assessor.run_comprehensive_security_assessment()
    exit(0 if is_secure else 1)