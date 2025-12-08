"""
Performance testing under load
"""
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

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

class PerformanceTester:
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
    
    def test_endpoint_response_time(self, url, method="GET", headers=None, data=None, iterations=10):
        """Test response time for a specific endpoint"""
        times = []
        
        for i in range(iterations):
            start_time = time.time()
            
            try:
                if method == "GET":
                    response = requests.get(url, headers=headers)
                elif method == "POST":
                    response = requests.post(url, headers=headers, json=data)
                elif method == "PATCH":
                    response = requests.patch(url, headers=headers, json=data)
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                times.append(response_time)
                
                if response.status_code not in [200, 201]:
                    print(f"⚠ Warning: Request returned status {response.status_code}")
                    
            except Exception as e:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                print(f"⚠ Request failed: {str(e)}")
        
        if times:
            avg_time = statistics.mean(times)
            min_time = min(times)
            max_time = max(times)
            return {
                "average": avg_time,
                "min": min_time,
                "max": max_time,
                "samples": len(times)
            }
        return None
    
    def test_concurrent_users(self, url, method="GET", headers=None, data=None, concurrent_users=5):
        """Test endpoint with concurrent users"""
        print(f"Testing {concurrent_users} concurrent users on {url}")
        
        def make_request():
            start_time = time.time()
            try:
                if method == "GET":
                    response = requests.get(url, headers=headers)
                elif method == "POST":
                    response = requests.post(url, headers=headers, json=data)
                elif method == "PATCH":
                    response = requests.patch(url, headers=headers, json=data)
                end_time = time.time()
                return (end_time - start_time) * 1000, response.status_code
            except Exception as e:
                end_time = time.time()
                return (end_time - start_time) * 1000, 0
        
        times = []
        statuses = []
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(make_request) for _ in range(concurrent_users)]
            
            for future in as_completed(futures):
                response_time, status_code = future.result()
                times.append(response_time)
                statuses.append(status_code)
        
        if times:
            avg_time = statistics.mean(times)
            success_rate = sum(1 for s in statuses if s in [200, 201]) / len(statuses) * 100
            return {
                "average_response_time": avg_time,
                "success_rate": success_rate,
                "total_requests": len(times)
            }
        return None
    
    def run_performance_tests(self):
        """Run comprehensive performance tests"""
        print("=" * 60)
        print("PERFORMANCE TESTING UNDER LOAD")
        print("=" * 60)
        
        if not self.admin_token or not self.owner_token:
            print("✗ Cannot run tests - authentication failed")
            return False
        
        # Define test endpoints
        test_endpoints = [
            {
                "name": "Admin Dashboard Stats",
                "url": f"{BASE_URL}/api/admin-module/dashboard-stats/",
                "method": "GET",
                "headers": {"Authorization": f"Token {self.admin_token}"}
            },
            {
                "name": "Property Owner Dashboard Stats",
                "url": f"{BASE_URL}/api/property-owner-module/dashboard-stats/",
                "method": "GET",
                "headers": {"Authorization": f"Token {self.owner_token}"}
            },
            {
                "name": "List Properties (Admin)",
                "url": f"{BASE_URL}/api/properties/",
                "method": "GET",
                "headers": {"Authorization": f"Token {self.admin_token}"}
            },
            {
                "name": "List Properties (Owner)",
                "url": f"{BASE_URL}/api/properties/",
                "method": "GET",
                "headers": {"Authorization": f"Token {self.owner_token}"}
            },
            {
                "name": "List Users",
                "url": f"{BASE_URL}/api/users/",
                "method": "GET",
                "headers": {"Authorization": f"Token {self.admin_token}"}
            }
        ]
        
        # Single user performance tests
        print("\nSingle User Performance Tests:")
        print("-" * 40)
        
        for endpoint in test_endpoints:
            result = self.test_endpoint_response_time(
                endpoint["url"],
                endpoint["method"],
                endpoint["headers"],
                iterations=5
            )
            
            if result:
                print(f"{endpoint['name']}:")
                print(f"  Average: {result['average']:.2f}ms")
                print(f"  Min: {result['min']:.2f}ms")
                print(f"  Max: {result['max']:.2f}ms")
                print(f"  Samples: {result['samples']}")
            else:
                print(f"✗ {endpoint['name']}: Test failed")
        
        # Concurrent user tests
        print("\nConcurrent User Tests:")
        print("-" * 40)
        
        for endpoint in test_endpoints[:3]:  # Test first 3 endpoints with concurrency
            result = self.test_concurrent_users(
                endpoint["url"],
                endpoint["method"],
                endpoint["headers"],
                concurrent_users=10
            )
            
            if result:
                print(f"{endpoint['name']} (10 concurrent users):")
                print(f"  Average Response Time: {result['average_response_time']:.2f}ms")
                print(f"  Success Rate: {result['success_rate']:.1f}%")
                print(f"  Total Requests: {result['total_requests']}")
            else:
                print(f"✗ {endpoint['name']}: Concurrent test failed")
        
        print("\n" + "=" * 60)
        print("PERFORMANCE TESTING COMPLETED")
        print("=" * 60)
        
        return True

if __name__ == "__main__":
    tester = PerformanceTester()
    tester.run_performance_tests()