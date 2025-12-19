"""
Performance monitoring utilities for the Property Management System.
"""

import time
import logging
from functools import wraps
from django.core.cache import cache
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)


def monitor_performance(func_name=None):
    """
    Decorator to monitor function performance and log slow operations.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            initial_queries = len(connection.queries)
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                query_count = len(connection.queries) - initial_queries
                
                # Log performance metrics
                func_display_name = func_name or func.__name__
                
                if execution_time > 1.0:  # Log slow operations (>1 second)
                    logger.warning(
                        f"Slow operation detected: {func_display_name} "
                        f"took {execution_time:.2f}s with {query_count} queries"
                    )
                elif settings.DEBUG:
                    logger.info(
                        f"Performance: {func_display_name} "
                        f"took {execution_time:.3f}s with {query_count} queries"
                    )
        
        return wrapper
    return decorator


class QueryCountDebugMixin:
    """
    Mixin to add query count debugging to views.
    """
    def dispatch(self, request, *args, **kwargs):
        if settings.DEBUG:
            initial_queries = len(connection.queries)
            
        response = super().dispatch(request, *args, **kwargs)
        
        if settings.DEBUG:
            query_count = len(connection.queries) - initial_queries
            if query_count > 10:  # Warn about high query counts
                logger.warning(
                    f"High query count in {self.__class__.__name__}: "
                    f"{query_count} queries for {request.method} {request.path}"
                )
        
        return response


class CacheManager:
    """
    Centralized cache management for the application.
    """
    
    # Cache timeouts (in seconds)
    CACHE_TIMEOUTS = {
        'user_stats': 300,      # 5 minutes
        'property_stats': 300,   # 5 minutes
        'dashboard_data': 180,   # 3 minutes
        'reports': 600,         # 10 minutes
    }
    
    @classmethod
    def get_cache_key(cls, key_type, *args):
        """Generate standardized cache keys."""
        return f"{key_type}:{'_'.join(str(arg) for arg in args)}"
    
    @classmethod
    def get_or_set(cls, key_type, key_args, callable_func, timeout=None):
        """
        Get from cache or set if not exists.
        """
        cache_key = cls.get_cache_key(key_type, *key_args)
        
        # Try to get from cache
        result = cache.get(cache_key)
        if result is not None:
            return result
        
        # Generate and cache the result
        result = callable_func()
        timeout = timeout or cls.CACHE_TIMEOUTS.get(key_type, 300)
        cache.set(cache_key, result, timeout)
        
        return result
    
    @classmethod
    def invalidate_pattern(cls, pattern):
        """
        Invalidate cache keys matching a pattern.
        Note: This is a simple implementation. For production,
        consider using Redis with pattern-based deletion.
        """
        # This is a basic implementation
        # In production, you might want to use Redis SCAN or similar
        pass
    
    @classmethod
    def invalidate_user_caches(cls, user_id):
        """Invalidate all caches related to a specific user."""
        patterns = [
            f"user_stats:{user_id}",
            f"dashboard_data:{user_id}",
            f"property_stats:*_{user_id}",
        ]
        for pattern in patterns:
            cache.delete(pattern)
    
    @classmethod
    def invalidate_property_caches(cls, property_id):
        """Invalidate all caches related to a specific property."""
        patterns = [
            f"property_stats:{property_id}",
            f"dashboard_data:*",  # Property changes affect dashboard
        ]
        for pattern in patterns:
            cache.delete(pattern)


def optimize_queryset(queryset, select_related=None, prefetch_related=None):
    """
    Helper function to optimize querysets with select_related and prefetch_related.
    """
    if select_related:
        queryset = queryset.select_related(*select_related)
    
    if prefetch_related:
        queryset = queryset.prefetch_related(*prefetch_related)
    
    return queryset


class DatabaseOptimizer:
    """
    Database optimization utilities.
    """
    
    @staticmethod
    def get_slow_queries(threshold=1.0):
        """
        Get queries that took longer than the threshold (in seconds).
        Only works in DEBUG mode.
        """
        if not settings.DEBUG:
            return []
        
        slow_queries = []
        for query in connection.queries:
            if float(query['time']) > threshold:
                slow_queries.append({
                    'sql': query['sql'],
                    'time': query['time']
                })
        
        return slow_queries
    
    @staticmethod
    def analyze_query_patterns():
        """
        Analyze query patterns to identify N+1 problems.
        Only works in DEBUG mode.
        """
        if not settings.DEBUG:
            return {}
        
        query_patterns = {}
        for query in connection.queries:
            sql = query['sql']
            # Simple pattern detection
            if 'SELECT' in sql and 'FROM' in sql:
                table_start = sql.find('FROM') + 5
                table_end = sql.find(' ', table_start)
                if table_end == -1:
                    table_end = len(sql)
                table_name = sql[table_start:table_end].strip()
                
                if table_name in query_patterns:
                    query_patterns[table_name] += 1
                else:
                    query_patterns[table_name] = 1
        
        return query_patterns


# Performance monitoring middleware
class PerformanceMonitoringMiddleware:
    """
    Middleware to monitor request performance.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        initial_queries = len(connection.queries) if settings.DEBUG else 0
        
        response = self.get_response(request)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        if settings.DEBUG:
            query_count = len(connection.queries) - initial_queries
            
            # Log slow requests
            if execution_time > 2.0:  # Requests taking more than 2 seconds
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {execution_time:.2f}s with {query_count} queries"
                )
            
            # Add performance headers in debug mode
            response['X-Debug-Query-Count'] = str(query_count)
            response['X-Debug-Execution-Time'] = f"{execution_time:.3f}s"
        
        return response