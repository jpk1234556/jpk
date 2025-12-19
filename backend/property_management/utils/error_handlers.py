"""
Enhanced error handling utilities for the Property Management System.
"""

import logging
import traceback
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404, HttpResponseServerError, HttpResponseForbidden, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
import sentry_sdk

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides more detailed error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Get the view and request from context
    view = context.get('view', None)
    request = context.get('request', None)
    
    # Extract user information if available
    user_info = "Anonymous"
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        user_info = f"{request.user.id}:{request.user.username}"
    
    # Log the error with context
    if response is not None:
        logger.error(
            f"API Error in {view.__class__.__name__ if view else 'Unknown'} "
            f"(Status: {response.status_code}) - User: {user_info} - "
            f"{exc.__class__.__name__}: {str(exc)}"
        )
        
        # Capture error in Sentry if available
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("view", view.__class__.__name__ if view else 'Unknown')
            scope.set_tag("user", user_info)
            scope.set_tag("status_code", response.status_code)
            sentry_sdk.capture_exception(exc)
    else:
        # For unhandled exceptions
        logger.error(
            f"Unhandled exception in {view.__class__.__name__ if view else 'Unknown'} "
            f"- User: {user_info} - {exc.__class__.__name__}: {str(exc)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        
        # Capture unhandled error in Sentry
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("view", view.__class__.__name__ if view else 'Unknown')
            scope.set_tag("user", user_info)
            sentry_sdk.capture_exception(exc)
    
    # Handle specific exceptions
    if isinstance(exc, ValidationError):
        return Response({
            'error': 'Validation Error',
            'message': str(exc),
            'details': exc.message_dict if hasattr(exc, 'message_dict') else None,
            'error_code': 'VALIDATION_ERROR'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, IntegrityError):
        return Response({
            'error': 'Database Integrity Error',
            'message': 'The operation violates database constraints',
            'details': str(exc),
            'error_code': 'INTEGRITY_ERROR'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, Http404):
        return Response({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'error_code': 'NOT_FOUND'
        }, status=status.HTTP_404_NOT_FOUND)
    
    elif isinstance(exc, PermissionDenied):
        return Response({
            'error': 'Permission Denied',
            'message': 'You do not have permission to perform this action',
            'error_code': 'PERMISSION_DENIED'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # If response is None, it means the exception wasn't handled by DRF
    if response is None:
        logger.error(f"Unhandled exception: {exc.__class__.__name__}: {str(exc)}")
        return Response({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'error_code': 'INTERNAL_ERROR'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Enhance the default response with more context
    if response.status_code >= 400:
        custom_response_data = {
            'error': response.data.get('detail', 'An error occurred'),
            'status_code': response.status_code,
            'error_code': get_error_code(response.status_code),
            'timestamp': context.get('request').META.get('HTTP_X_TIMESTAMP') if context.get('request') else None
        }
        
        # Add field-specific errors if they exist
        if isinstance(response.data, dict) and 'detail' not in response.data:
            custom_response_data['field_errors'] = response.data
        
        response.data = custom_response_data
    
    return response


def get_error_code(status_code):
    """Map HTTP status codes to error codes."""
    error_codes = {
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
        403: 'FORBIDDEN',
        404: 'NOT_FOUND',
        405: 'METHOD_NOT_ALLOWED',
        409: 'CONFLICT',
        422: 'UNPROCESSABLE_ENTITY',
        429: 'TOO_MANY_REQUESTS',
        500: 'INTERNAL_SERVER_ERROR',
        502: 'BAD_GATEWAY',
        503: 'SERVICE_UNAVAILABLE',
        504: 'GATEWAY_TIMEOUT'
    }
    return error_codes.get(status_code, 'UNKNOWN_ERROR')


def custom_page_not_found(request, exception):
    """Custom 404 error handler."""
    logger.warning(f"404 Error: {request.path} not found. User: {request.user.id if request.user.is_authenticated else 'Anonymous'}")
    return render(request, '404.html', {'exception': exception}, status=404)


def custom_server_error(request):
    """Custom 500 error handler."""
    logger.error(f"500 Error: Internal server error. User: {request.user.id if request.user.is_authenticated else 'Anonymous'}")
    return render(request, '500.html', status=500)


def custom_permission_denied(request, exception):
    """Custom 403 error handler."""
    logger.warning(f"403 Error: Permission denied. User: {request.user.id if request.user.is_authenticated else 'Anonymous'}")
    return render(request, '403.html', {'exception': exception}, status=403)


def custom_bad_request(request, exception):
    """Custom 400 error handler."""
    logger.warning(f"400 Error: Bad request. User: {request.user.id if request.user.is_authenticated else 'Anonymous'}")
    return render(request, '400.html', {'exception': exception}, status=400)


class APIErrorMixin:
    """
    Mixin to provide consistent error responses across views.
    """
    
    def handle_error(self, error_message, status_code=status.HTTP_400_BAD_REQUEST, details=None, error_code=None):
        """
        Create a standardized error response.
        """
        error_data = {
            'error': error_message,
            'status_code': status_code,
            'error_code': error_code or get_error_code(status_code)
        }
        
        if details:
            error_data['details'] = details
        
        logger.warning(f"API Error: {error_message} - Details: {details}")
        return Response(error_data, status=status_code)
    
    def handle_validation_error(self, serializer):
        """
        Handle serializer validation errors.
        """
        return self.handle_error(
            'Validation failed',
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
            'VALIDATION_ERROR'
        )
    
    def handle_not_found(self, resource_name="Resource"):
        """
        Handle not found errors.
        """
        return self.handle_error(
            f'{resource_name} not found',
            status.HTTP_404_NOT_FOUND,
            error_code='NOT_FOUND'
        )
    
    def handle_permission_denied(self, message="Permission denied"):
        """
        Handle permission denied errors.
        """
        return self.handle_error(
            message,
            status.HTTP_403_FORBIDDEN,
            error_code='PERMISSION_DENIED'
        )


class ValidationMixin:
    """
    Mixin to provide enhanced validation capabilities.
    """
    
    def validate_user_permissions(self, user, required_role=None, required_approval=True):
        """
        Validate user permissions.
        """
        if not user.is_authenticated:
            raise ValidationError("Authentication required")
        
        if required_approval and not user.is_approved:
            raise ValidationError("Account approval required")
        
        if required_role and user.role != required_role:
            raise ValidationError(f"Role '{required_role}' required")
    
    def validate_ownership(self, user, obj, owner_field='owner'):
        """
        Validate that user owns the object.
        """
        if user.role == 'admin':
            return True  # Admins can access everything
        
        owner = getattr(obj, owner_field, None)
        if owner != user:
            raise ValidationError("You don't have permission to access this resource")
        
        return True
    
    def validate_required_fields(self, data, required_fields):
        """
        Validate that required fields are present.
        """
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationError(f"Required fields missing: {', '.join(missing_fields)}")


class BusinessLogicValidator:
    """
    Validator for business logic rules.
    """
    
    @staticmethod
    def validate_property_owner_assignment(property_obj, owner):
        """
        Validate property owner assignment.
        """
        if owner.role != 'property_owner':
            raise ValidationError("Only users with 'property_owner' role can own properties")
        
        if not owner.is_approved:
            raise ValidationError("Property owner must be approved")
    
    @staticmethod
    def validate_unit_capacity(unit, tenant_count):
        """
        Validate unit capacity constraints.
        """
        if tenant_count > unit.capacity:
            raise ValidationError(f"Unit capacity exceeded. Maximum: {unit.capacity}")
    
    @staticmethod
    def validate_lease_dates(start_date, end_date):
        """
        Validate lease date constraints.
        """
        from datetime import date
        
        if start_date > end_date:
            raise ValidationError("Lease start date cannot be after end date")
        
        if end_date < date.today():
            raise ValidationError("Lease end date cannot be in the past")
    
    @staticmethod
    def validate_payment_amount(payment_amount, expected_amount, tolerance=0.01):
        """
        Validate payment amounts.
        """
        if abs(payment_amount - expected_amount) > tolerance:
            raise ValidationError(
                f"Payment amount {payment_amount} doesn't match expected amount {expected_amount}"
            )


def log_api_error(view_name, error, request_data=None):
    """
    Log API errors with context.
    """
    logger.error(
        f"API Error in {view_name}: {error.__class__.__name__}: {str(error)}",
        extra={
            'view': view_name,
            'error_type': error.__class__.__name__,
            'error_message': str(error),
            'request_data': request_data
        }
    )


def handle_database_error(func):
    """
    Decorator to handle common database errors.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            logger.error(f"Database integrity error in {func.__name__}: {str(e)}")
            raise ValidationError("Operation violates database constraints")
        except Exception as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            raise
    
    return wrapper


class PerformanceLogger:
    """
    Utility class for logging performance metrics.
    """
    
    @staticmethod
    def log_endpoint_performance(view_name, execution_time, user_id=None):
        """
        Log endpoint performance metrics.
        """
        logger.info(
            f"Performance: {view_name} executed in {execution_time:.4f}s",
            extra={
                'view': view_name,
                'execution_time': execution_time,
                'user_id': user_id,
                'metric': 'endpoint_performance'
            },
            extra_logger='property_management.performance'
        )
    
    @staticmethod
    def log_cache_hit(cache_key, view_name):
        """
        Log cache hit events.
        """
        logger.info(
            f"Cache hit: {cache_key} in {view_name}",
            extra={
                'cache_key': cache_key,
                'view': view_name,
                'metric': 'cache_hit'
            },
            extra_logger='property_management.performance'
        )
    
    @staticmethod
    def log_cache_miss(cache_key, view_name):
        """
        Log cache miss events.
        """
        logger.info(
            f"Cache miss: {cache_key} in {view_name}",
            extra={
                'cache_key': cache_key,
                'view': view_name,
                'metric': 'cache_miss'
            },
            extra_logger='property_management.performance'
        )


class AnalyticsLogger:
    """
    Utility class for logging user analytics and behavior.
    """
    
    @staticmethod
    def log_user_action(user_id, action, resource_type=None, resource_id=None, metadata=None):
        """
        Log user actions for analytics.
        """
        logger.info(
            f"User Action: {user_id} performed {action}",
            extra={
                'user_id': user_id,
                'action': action,
                'resource_type': resource_type,
                'resource_id': resource_id,
                'metadata': metadata,
                'metric': 'user_action'
            },
            extra_logger='property_management.analytics'
        )
    
    @staticmethod
    def log_feature_usage(user_id, feature_name, metadata=None):
        """
        Log feature usage for analytics.
        """
        logger.info(
            f"Feature Usage: {user_id} used {feature_name}",
            extra={
                'user_id': user_id,
                'feature': feature_name,
                'metadata': metadata,
                'metric': 'feature_usage'
            },
            extra_logger='property_management.analytics'
        )