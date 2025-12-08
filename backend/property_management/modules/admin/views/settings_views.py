from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
import json


class AdminSettingsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    # In a real application, this would be stored in a database
    # For this example, we'll use an in-memory store
    _settings = {
        'company_info': {
            'name': 'Property Management Inc.',
            'address': '123 Business Street, Suite 100, City, State 12345',
            'phone': '(555) 123-4567',
            'email': 'info@propertymanagement.com'
        },
        'currency_locale': {
            'currency': 'USD',
            'timezone': 'EST'
        },
        'property_settings': {
            'default_lease_term': 12,
            'grace_period': 5
        },
        'notifications': {
            'rent_due': True,
            'maintenance': True,
            'lease_expiry': True,
            'payment_received': True,
            'frequency': 'immediate',
            'email': 'notifications@propertymanagement.com'
        },
        'security': {
            'min_password_length': 8,
            'require_special_chars': True,
            'require_numbers': True,
            'require_uppercase': True,
            'session_timeout': 30,
            'enable_2fa': True
        },
        'integrations': {
            'payment_gateway': 'stripe',
            'api_key': 'sk_test_*********************',
            'google_maps': True,
            'sms': True,
            'cloud_storage': True
        }
    }
    
    def get(self, request):
        # Check if user is admin
        if not (hasattr(request.user, 'role') and request.user.role == 'admin'):
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(self._settings)
    
    def patch(self, request):
        # Check if user is admin
        if not (hasattr(request.user, 'role') and request.user.role == 'admin'):
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Update settings based on request data
        data = request.data
        
        # Update each section if provided
        if 'company_info' in data:
            self._settings['company_info'].update(data['company_info'])
        
        if 'currency_locale' in data:
            self._settings['currency_locale'].update(data['currency_locale'])
        
        if 'property_settings' in data:
            self._settings['property_settings'].update(data['property_settings'])
        
        if 'notifications' in data:
            self._settings['notifications'].update(data['notifications'])
        
        if 'security' in data:
            self._settings['security'].update(data['security'])
        
        if 'integrations' in data:
            self._settings['integrations'].update(data['integrations'])
        
        return Response({
            'message': 'Settings updated successfully',
            'settings': self._settings
        })