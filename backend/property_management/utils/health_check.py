"""
Health check utilities for the Property Management System.
"""

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .monitoring import HealthCheckService
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Comprehensive health check endpoint.
    """
    logger.info("Health check requested")
    
    # Perform health checks
    overall_status, results = HealthCheckService.perform_health_check()
    
    # Prepare response data
    health_data = {
        'status': 'healthy' if overall_status else 'unhealthy',
        'checks': {},
        'timestamp': timezone.now().isoformat()
    }
    
    # Add individual check results
    for check_name, (check_status, check_message) in results.items():
        health_data['checks'][check_name] = {
            'status': 'healthy' if check_status else 'unhealthy',
            'message': check_message
        }
    
    # Set appropriate HTTP status code
    status_code = 200 if overall_status else 503
    
    logger.info(f"Health check completed - Status: {health_data['status']}")
    
    return Response(health_data, status=status_code)


@api_view(['GET'])
@permission_classes([AllowAny])
def simple_health_check(request):
    """
    Simple health check endpoint for uptime monitoring.
    """
    return Response({'status': 'ok'}, status=200)