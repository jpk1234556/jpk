"""
Monitoring utilities for the Property Management System.
"""

import time
import logging
import psutil
import os
from functools import wraps
from django.conf import settings
from .error_handlers import PerformanceLogger, AnalyticsLogger

logger = logging.getLogger('property_management.performance')


class MonitoringMiddleware:
    """
    Middleware to monitor request performance and collect metrics.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Record start time
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Log performance metrics
        view_name = getattr(request.resolver_match, 'view_name', 'unknown')
        user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
        
        PerformanceLogger.log_endpoint_performance(view_name, execution_time, user_id)
        
        # Add performance header
        response['X-Response-Time'] = f"{execution_time:.4f}s"
        
        return response


class HealthCheckService:
    """
    Service to perform health checks on various system components.
    """
    
    @staticmethod
    def check_database_connection():
        """Check database connectivity."""
        from django.db import connection
        try:
            connection.cursor()
            return True, "Database connection successful"
        except Exception as e:
            return False, f"Database connection failed: {str(e)}"
    
    @staticmethod
    def check_cache_connection():
        """Check cache connectivity."""
        from django.core.cache import cache
        try:
            cache.set('health_check', 'test', 30)
            result = cache.get('health_check')
            if result == 'test':
                return True, "Cache connection successful"
            else:
                return False, "Cache connection failed: Unable to retrieve test value"
        except Exception as e:
            return False, f"Cache connection failed: {str(e)}"
    
    @staticmethod
    def check_disk_space():
        """Check available disk space."""
        try:
            disk_usage = psutil.disk_usage('/')
            free_percent = (disk_usage.free / disk_usage.total) * 100
            if free_percent < 10:  # Less than 10% free
                return False, f"Low disk space: {free_percent:.2f}% free"
            return True, f"Disk space OK: {free_percent:.2f}% free"
        except Exception as e:
            return False, f"Unable to check disk space: {str(e)}"
    
    @staticmethod
    def check_memory_usage():
        """Check system memory usage."""
        try:
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            if memory_percent > 90:  # More than 90% used
                return False, f"High memory usage: {memory_percent:.2f}% used"
            return True, f"Memory usage OK: {memory_percent:.2f}% used"
        except Exception as e:
            return False, f"Unable to check memory usage: {str(e)}"
    
    @staticmethod
    def perform_health_check():
        """Perform comprehensive health check."""
        results = {
            'database': HealthCheckService.check_database_connection(),
            'cache': HealthCheckService.check_cache_connection(),
            'disk_space': HealthCheckService.check_disk_space(),
            'memory': HealthCheckService.check_memory_usage(),
        }
        
        overall_status = all(result[0] for result in results.values())
        return overall_status, results


def monitor_performance(view_func):
    """
    Decorator to monitor view performance.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        try:
            result = view_func(request, *args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            view_name = f"{view_func.__module__}.{view_func.__name__}"
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            
            PerformanceLogger.log_endpoint_performance(view_name, execution_time, user_id)
            
            # Log slow requests (>1 second)
            if execution_time > 1.0:
                logger.warning(f"Slow request detected: {view_name} took {execution_time:.4f}s")
    
    return wrapper


class AlertManager:
    """
    Simple alert manager for system monitoring.
    """
    
    @staticmethod
    def send_alert(message, level='warning'):
        """
        Send an alert based on severity level.
        """
        logger_func = {
            'info': logger.info,
            'warning': logger.warning,
            'error': logger.error,
            'critical': logger.critical
        }.get(level, logger.warning)
        
        logger_func(f"ALERT [{level.upper()}]: {message}")
        
        # In a production environment, you might want to send alerts via email,
        # Slack, or other notification services
        if level in ['error', 'critical']:
            # This is where you'd integrate with external alerting systems
            pass


# System metrics collector
class SystemMetricsCollector:
    """
    Collects system-level metrics for monitoring.
    """
    
    @staticmethod
    def get_system_metrics():
        """Get current system metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            metrics = {
                'cpu_percent': cpu_percent,
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'memory_used_gb': round(memory.used / (1024**3), 2),
                'memory_percent': memory.percent,
                'disk_total_gb': round(disk.total / (1024**3), 2),
                'disk_used_gb': round(disk.used / (1024**3), 2),
                'disk_percent': round((disk.used / disk.total) * 100, 2),
            }
            
            return metrics
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            return {}


# Request counter for tracking usage
class RequestCounter:
    """
    Tracks API request counts and patterns.
    """
    
    def __init__(self):
        self.counts = {}
    
    def increment(self, endpoint, method, user_id=None):
        """Increment request count for an endpoint."""
        key = f"{method}:{endpoint}"
        if key not in self.counts:
            self.counts[key] = 0
        self.counts[key] += 1
        
        # Log usage analytics
        AnalyticsLogger.log_feature_usage(
            user_id=user_id,
            feature_name=f"{method} {endpoint}",
            metadata={'request_count': self.counts[key]}
        )
    
    def get_counts(self):
        """Get current request counts."""
        return self.counts.copy()


# Global request counter instance
request_counter = RequestCounter()