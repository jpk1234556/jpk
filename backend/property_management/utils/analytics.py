"""
Analytics utilities for tracking user behavior and system usage.
"""

import logging
from datetime import datetime
from django.utils import timezone
from .error_handlers import AnalyticsLogger

logger = logging.getLogger('property_management.analytics')


class UserBehaviorTracker:
    """
    Tracks user behavior and interactions with the system.
    """
    
    @staticmethod
    def track_login(user_id, ip_address=None, user_agent=None):
        """Track user login events."""
        AnalyticsLogger.log_user_action(
            user_id=user_id,
            action='login',
            metadata={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'timestamp': timezone.now().isoformat()
            }
        )
    
    @staticmethod
    def track_logout(user_id):
        """Track user logout events."""
        AnalyticsLogger.log_user_action(
            user_id=user_id,
            action='logout',
            metadata={
                'timestamp': timezone.now().isoformat()
            }
        )
    
    @staticmethod
    def track_page_view(user_id, page_url, page_title=None):
        """Track page views."""
        AnalyticsLogger.log_user_action(
            user_id=user_id,
            action='page_view',
            resource_type='page',
            resource_id=page_url,
            metadata={
                'page_title': page_title,
                'timestamp': timezone.now().isoformat()
            }
        )
    
    @staticmethod
    def track_feature_usage(user_id, feature_name, action='use', metadata=None):
        """Track feature usage."""
        if metadata is None:
            metadata = {}
        metadata['timestamp'] = timezone.now().isoformat()
        
        AnalyticsLogger.log_feature_usage(
            user_id=user_id,
            feature_name=feature_name,
            metadata=metadata
        )
    
    @staticmethod
    def track_form_submission(user_id, form_name, success=True, errors=None):
        """Track form submissions."""
        AnalyticsLogger.log_user_action(
            user_id=user_id,
            action='form_submit',
            resource_type='form',
            resource_id=form_name,
            metadata={
                'success': success,
                'errors': errors,
                'timestamp': timezone.now().isoformat()
            }
        )


class FeatureUsageAnalytics:
    """
    Analytics for tracking feature adoption and usage patterns.
    """
    
    def __init__(self):
        self.feature_usage = {}
    
    def record_feature_use(self, feature_name, user_id=None):
        """Record feature usage."""
        if feature_name not in self.feature_usage:
            self.feature_usage[feature_name] = {
                'total_uses': 0,
                'unique_users': set(),
                'first_used': timezone.now(),
            }
        
        self.feature_usage[feature_name]['total_uses'] += 1
        if user_id:
            self.feature_usage[feature_name]['unique_users'].add(user_id)
    
    def get_feature_stats(self, feature_name):
        """Get statistics for a specific feature."""
        if feature_name not in self.feature_usage:
            return None
        
        feature_data = self.feature_usage[feature_name]
        return {
            'total_uses': feature_data['total_uses'],
            'unique_users': len(feature_data['unique_users']),
            'first_used': feature_data['first_used'],
            'last_used': timezone.now(),
        }
    
    def get_all_features_stats(self):
        """Get statistics for all features."""
        stats = {}
        for feature_name in self.feature_usage:
            stats[feature_name] = self.get_feature_stats(feature_name)
        return stats


class SystemUsageAnalytics:
    """
    Analytics for tracking overall system usage and performance.
    """
    
    def __init__(self):
        self.daily_active_users = set()
        self.daily_requests = 0
        self.current_day = datetime.now().date()
    
    def record_user_activity(self, user_id):
        """Record user activity for daily active users calculation."""
        today = datetime.now().date()
        # Reset counters if it's a new day
        if today != self.current_day:
            self.daily_active_users = set()
            self.daily_requests = 0
            self.current_day = today
        
        self.daily_active_users.add(user_id)
        self.daily_requests += 1
    
    def get_daily_stats(self):
        """Get daily usage statistics."""
        return {
            'daily_active_users': len(self.daily_active_users),
            'daily_requests': self.daily_requests,
            'date': self.current_day.isoformat(),
        }


# Global instances
feature_analytics = FeatureUsageAnalytics()
system_analytics = SystemUsageAnalytics()


class AnalyticsMiddleware:
    """
    Middleware to automatically track user interactions and system usage.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Record system usage
        if hasattr(request, 'user') and request.user.is_authenticated:
            system_analytics.record_user_activity(request.user.id)
            # Track page views for GET requests
            if request.method == 'GET':
                UserBehaviorTracker.track_page_view(
                    user_id=request.user.id,
                    page_url=request.path,
                    page_title=getattr(request, 'title', None)
                )
        
        response = self.get_response(request)
        return response


class ReportGenerator:
    """
    Generates analytics reports.
    """
    
    @staticmethod
    def generate_daily_report():
        """Generate a daily analytics report."""
        daily_stats = system_analytics.get_daily_stats()
        feature_stats = feature_analytics.get_all_features_stats()
        
        report = {
            'report_date': timezone.now().isoformat(),
            'daily_stats': daily_stats,
            'feature_usage': feature_stats,
        }
        
        logger.info(f"Daily Analytics Report Generated: {report}")
        return report
    
    @staticmethod
    def generate_user_engagement_report():
        """Generate a user engagement report."""
        # This would typically query the database for more detailed metrics
        report = {
            'report_date': timezone.now().isoformat(),
            'active_users_today': len(system_analytics.daily_active_users),
            'features_tracked': len(feature_analytics.feature_usage),
        }
        
        logger.info(f"User Engagement Report Generated: {report}")
        return report