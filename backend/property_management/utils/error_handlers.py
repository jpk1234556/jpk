"""
Enhanced error handling utilities for the Property Management System.
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404

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
    
    # Log the error
    if response is not None:
        logger.error(
            f"API Error in {view.__class__.__name__ if view else 'Unknown'}: "
            f"{exc.__class__.__name__}: {str(exc)}"
        )
    
    # Handle specific exceptions
    if isinstance(exc, ValidationError):
        return Response({
            'error': 'Validation Error',
            'message': str(exc),
            'details': exc.message_dict if hasattr(exc, 'message_dict') else None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, IntegrityError):
        return Response({
            'error': 'Database Integrity Error',
            'message': 'The operation violates database constraints',
            'details': str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, Http404):
        return Response({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # If response is None, it means the exception wasn't handled by DRF
    if response is None:
        logger.error(f"Unhandled exception: {exc.__class__.__name__}: {str(exc)}")
        return Response({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Enhance the default response with more context
    if response.status_code >= 400:
        custom_response_data = {
            'error': response.data.get('detail', 'An error occurred'),
            'status_code': response.status_code,
            'timestamp': context.get('request').META.get('HTTP_X_TIMESTAMP') if context.get('request') else None
        }
        
        # Add field-specific errors if they exist
        if isinstance(response.data, dict) and 'detail' not in response.data:
            custom_response_data['field_errors'] = response.data
        
        response.data = custom_response_data
    
    return response


class APIErrorMixin:
    """
    Mixin to provide consistent error responses across views.
    """
    
    def handle_error(self, error_message, status_code=status.HTTP_400_BAD_REQUEST, details=None):
        """
        Create a standardized error response.
        """
        error_data = {
            'error': error_message,
            'status_code': status_code
        }
        
        if details:
            error_data['details'] = details
        
        return Response(error_data, status=status_code)
    
    def handle_validation_error(self, serializer):
        """
        Handle serializer validation errors.
        """
        return self.handle_error(
            'Validation failed',
            status.HTTP_400_BAD_REQUEST,
            serializer.errors
        )
    
    def handle_not_found(self, resource_name="Resource"):
        """
        Handle not found errors.
        """
        return self.handle_error(
            f'{resource_name} not found',
            status.HTTP_404_NOT_FOUND
        )
    
    def handle_permission_denied(self, message="Permission denied"):
        """
        Handle permission denied errors.
        """
        return self.handle_error(
            message,
            status.HTTP_403_FORBIDDEN
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