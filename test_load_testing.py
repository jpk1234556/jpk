"""
Enhanced Load Testing for Concurrent Users
"""

import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics
import csv
import json
from datetime import datetime
import psutil
import os

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

class LoadTester:
    def __init__(self):
        self.admin_token = None
        self.owner_token = None
        self.setup_tokens()
        self.results = []
    
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
    
    def measure_system_resources(self):
        """Measure system resources during testing"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024)
            }
        except Exception as e:
            print(f"⚠ Resource measurement error: {str(e)}")
            return {"cpu_percent": 0, "memory_percent": 0, "memory_available_mb": 0}
    
    def make_request(self, url, method="GET", headers=None, data=None, user_id=None):
        """Make a single request and return timing and status information"""
        start_time = time.time()
        start_resources = self.measure_system_resources()
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=30)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            
            end_time = time.time()
            end_resources = self.measure_system_resources()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            return {
                "user_id": user_id,
                "url": url,
                "method": method,
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "success": response.status_code in [200, 201, 204],
                "start_time": start_time,
                "end_time": end_time,
                "cpu_before": start_resources["cpu_percent"],
                "cpu_after": end_resources["cpu_percent"],
                "memory_before": start_resources["memory_percent"],
                "memory_after": end_resources["memory_percent"]
            }
        except requests.exceptions.Timeout:
            end_time = time.time()
            end_resources = self.measure_system_resources()
            response_time = (end_time - start_time) * 1000
            
            return {
                "user_id": user_id,
                "url": url,
                "method": method,
                "status_code": 408,  # Timeout
                "response_time_ms": response_time,
                "success": False,
                "start_time": start_time,
                "end_time": end_time,
                "cpu_before": start_resources["cpu_percent"],
                "cpu_after": end_resources["cpu_percent"],
                "memory_before": start_resources["memory_percent"],
                "memory_after": end_resources["memory_percent"]
            }
        except Exception as e:
            end_time = time.time()
            end_resources = self.measure_system_resources()
            response_time = (end_time - start_time) * 1000
            
            return {
                "user_id": user_id,
                "url": url,
                "method": method,
                "status_code": 0,  # Connection error
                "response_time_ms": response_time,
                "success": False,
                "error": str(e),
                "start_time": start_time,
                "end_time": end_time,
                "cpu_before": start_resources["cpu_percent"],
                "cpu_after": end_resources["cpu_percent"],
                "memory_before": start_resources["memory_percent"],
                "memory_after": end_resources["memory_percent"]
            }
    
    def run_concurrent_test(self, url, method="GET", headers=None, data=None, 
                           concurrent_users=10, duration_seconds=60, ramp_up_seconds=10):
        """
        Run a sustained load test with concurrent users for a specified duration
        
        Args:
            url: Target URL
            method: HTTP method
            headers: Request headers
            data: Request data
            concurrent_users: Number of concurrent users
            duration_seconds: Test duration in seconds
            ramp_up_seconds: Time to ramp up users
        """
        print(f"\nRunning load test: {concurrent_users} users for {duration_seconds} seconds")
        print(f"Target: {method} {url}")
        
        results = []
        start_test_time = time.time()
        end_test_time = start_test_time + duration_seconds
        
        def user_worker(user_id):
            """Worker function for each simulated user"""
            user_results = []
            
            # Ramp up delay
            ramp_delay = (user_id / concurrent_users) * ramp_up_seconds
            time.sleep(ramp_delay)
            
            while time.time() < end_test_time:
                result = self.make_request(url, method, headers, data, user_id)
                user_results.append(result)
                
                # Small delay between requests to simulate real user behavior
                time.sleep(0.1)
            
            return user_results
        
        # Run the test
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # Submit all user workers
            futures = [executor.submit(user_worker, i) for i in range(concurrent_users)]
            
            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    user_results = future.result(timeout=duration_seconds + 10)
                    results.extend(user_results)
                except Exception as e:
                    print(f"⚠ User worker error: {str(e)}")
        
        return results
    
    def run_scalability_test(self, url, method="GET", headers=None, data=None):
        """
        Run scalability tests with increasing user loads
        """
        print(f"\n{'='*60}")
        print(f"SCALABILITY TEST: {method} {url}")
        print(f"{'='*60}")
        
        user_levels = [10, 50, 100, 200, 500]
        test_duration = 30  # seconds
        results_summary = []
        
        for user_count in user_levels:
            print(f"\nTesting with {user_count} concurrent users...")
            
            # Skip high user counts if we don't have auth tokens
            if not self.admin_token and not self.owner_token:
                print("✗ Skipping test - no authentication tokens available")
                continue
            
            # Select appropriate token based on endpoint
            test_headers = headers.copy() if headers else {}
            if "/admin" in url and self.admin_token:
                test_headers["Authorization"] = f"Token {self.admin_token}"
            elif "/owner" in url and self.owner_token:
                test_headers["Authorization"] = f"Token {self.owner_token}"
            
            try:
                results = self.run_concurrent_test(
                    url, method, test_headers, data,
                    concurrent_users=user_count,
                    duration_seconds=test_duration
                )
                
                # Analyze results
                successful_requests = [r for r in results if r["success"]]
                failed_requests = [r for r in results if not r["success"]]
                response_times = [r["response_time_ms"] for r in successful_requests]
                
                if response_times:
                    avg_response_time = statistics.mean(response_times)
                    percentile_95 = sorted(response_times)[int(len(response_times) * 0.95)]
                    success_rate = len(successful_requests) / len(results) * 100
                    
                    summary = {
                        "users": user_count,
                        "total_requests": len(results),
                        "successful_requests": len(successful_requests),
                        "failed_requests": len(failed_requests),
                        "success_rate": success_rate,
                        "avg_response_time_ms": avg_response_time,
                        "p95_response_time_ms": percentile_95,
                        "requests_per_second": len(results) / test_duration
                    }
                    
                    results_summary.append(summary)
                    
                    print(f"  ✓ Results for {user_count} users:")
                    print(f"    Success Rate: {success_rate:.1f}%")
                    print(f"    Avg Response Time: {avg_response_time:.2f}ms")
                    print(f"    95th Percentile: {percentile_95:.2f}ms")
                    print(f"    Requests/sec: {summary['requests_per_second']:.2f}")
                else:
                    print(f"  ✗ No successful requests for {user_count} users")
                    
            except Exception as e:
                print(f"  ✗ Test failed for {user_count} users: {str(e)}")
        
        return results_summary
    
    def run_stress_test(self, url, method="GET", headers=None, data=None, max_users=1000):
        """
        Run stress test to find breaking point
        """
        print(f"\n{'='*60}")
        print(f"STRESS TEST: {method} {url}")
        print(f"{'='*60}")
        
        user_count = 10
        step_size = 50
        max_failures = 5
        failure_count = 0
        results = []
        
        while user_count <= max_users and failure_count < max_failures:
            print(f"\nStress testing with {user_count} concurrent users...")
            
            try:
                test_results = self.run_concurrent_test(
                    url, method, headers, data,
                    concurrent_users=user_count,
                    duration_seconds=15  # Shorter duration for stress test
                )
                
                successful_requests = [r for r in test_results if r["success"]]
                success_rate = len(successful_requests) / len(test_results) * 100
                
                print(f"  Success Rate: {success_rate:.1f}%")
                
                if success_rate < 95:  # Consider it a failure if success rate drops below 95%
                    failure_count += 1
                    print(f"  ⚠ Low success rate - failure count: {failure_count}")
                else:
                    failure_count = 0  # Reset failure count on success
                
                results.append({
                    "users": user_count,
                    "success_rate": success_rate,
                    "total_requests": len(test_results)
                })
                
                user_count += step_size
                
            except Exception as e:
                print(f"  ✗ Test failed: {str(e)}")
                failure_count += 1
        
        if failure_count >= max_failures:
            print(f"\n⚠ Breaking point reached at approximately {user_count - step_size} users")
        else:
            print(f"\n✓ System handled up to {user_count - step_size} users successfully")
        
        return results
    
    def save_results_to_csv(self, results, filename=None):
        """Save test results to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"load_test_results_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = results[0].keys() if results else []
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for result in results:
                    writer.writerow(result)
            
            print(f"✓ Results saved to {filename}")
            return filename
        except Exception as e:
            print(f"✗ Failed to save results: {str(e)}")
            return None
    
    def generate_report(self, scalability_results, stress_results):
        """Generate a comprehensive test report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = {
            "timestamp": timestamp,
            "scalability_test": scalability_results,
            "stress_test": stress_results,
            "system_info": {
                "platform": os.name,
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": psutil.virtual_memory().total / (1024**3)
            }
        }
        
        # Save report to JSON file
        report_filename = f"load_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"✓ Detailed report saved to {report_filename}")
        except Exception as e:
            print(f"✗ Failed to save report: {str(e)}")
        
        return report
    
    def run_comprehensive_load_tests(self):
        """Run comprehensive load testing suite"""
        print("=" * 70)
        print("COMPREHENSIVE LOAD TESTING SUITE")
        print("=" * 70)
        
        if not self.admin_token and not self.owner_token:
            print("✗ Cannot run tests - authentication failed")
            return False
        
        # Define test endpoints
        test_endpoints = [
            {
                "name": "Admin Dashboard Stats",
                "url": f"{BASE_URL}/api/admin-module/dashboard-stats/",
                "method": "GET",
                "headers": {"Authorization": f"Token {self.admin_token}"} if self.admin_token else {}
            },
            {
                "name": "Property Owner Dashboard Stats",
                "url": f"{BASE_URL}/api/property-owner-module/dashboard-stats/",
                "method": "GET",
                "headers": {"Authorization": f"Token {self.owner_token}"} if self.owner_token else {}
            },
            {
                "name": "List Properties (Admin)",
                "url": f"{BASE_URL}/api/properties/",
                "method": "GET",
                "headers": {"Authorization": f"Token {self.admin_token}"} if self.admin_token else {}
            }
        ]
        
        all_scalability_results = []
        all_stress_results = []
        
        # Run tests for each endpoint
        for endpoint in test_endpoints:
            print(f"\n{'#' * 70}")
            print(f"TESTING ENDPOINT: {endpoint['name']}")
            print(f"{'#' * 70}")
            
            # Skip if we don't have the required token
            if ("/admin" in endpoint["url"] and not self.admin_token) or \
               ("/owner" in endpoint["url"] and not self.owner_token):
                print(f"⚠ Skipping {endpoint['name']} - missing required authentication")
                continue
            
            # Scalability test
            scalability_results = self.run_scalability_test(
                endpoint["url"],
                endpoint["method"],
                endpoint["headers"]
            )
            all_scalability_results.extend([
                {**result, "endpoint": endpoint["name"]} 
                for result in scalability_results
            ])
            
            # Stress test
            stress_results = self.run_stress_test(
                endpoint["url"],
                endpoint["method"],
                endpoint["headers"],
                max_users=500  # Limit for stress test
            )
            all_stress_results.extend([
                {**result, "endpoint": endpoint["name"]} 
                for result in stress_results
            ])
        
        # Generate final report
        if all_scalability_results or all_stress_results:
            self.generate_report(all_scalability_results, all_stress_results)
            print(f"\n{'=' * 70}")
            print("LOAD TESTING COMPLETED SUCCESSFULLY")
            print(f"{'=' * 70}")
            return True
        else:
            print(f"\n{'=' * 70}")
            print("LOAD TESTING FAILED - NO RESULTS GENERATED")
            print(f"{'=' * 70}")
            return False

if __name__ == "__main__":
    tester = LoadTester()
    success = tester.run_comprehensive_load_tests()
    exit(0 if success else 1)