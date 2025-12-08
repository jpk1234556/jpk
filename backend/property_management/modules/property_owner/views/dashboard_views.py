from rest_framework import generics, permissions
from rest_framework.response import Response
import logging
from apps.properties.models import Property

# Set up logging
logger = logging.getLogger(__name__)

class PropertyOwnerDashboardStatsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            # Check if user is property owner
            if hasattr(request.user, 'role') and request.user.role == 'property_owner':
                # Get properties owned by this user
                properties = Property.objects.filter(owner=request.user)
                my_properties = properties.count()
                
                # Calculate units statistics
                total_units = 0
                occupied_units = 0
                
                for prop in properties:
                    # We would need to implement these fields in the Property model
                    total_units += getattr(prop, 'units', 0) or 0
                    occupied_units += getattr(prop, 'occupied', 0) or 0
                
                pending_requests = 2  # Mock data for now
                
                stats = {
                    'myProperties': my_properties,
                    'totalUnits': total_units,
                    'occupiedUnits': occupied_units,
                    'pendingRequests': pending_requests
                }
                
                return Response(stats)
            else:
                # Return forbidden for non-property owner users
                return Response({'error': 'Access denied. Property owner access required.'}, status=403)
        except Exception as e:
            logger.error(f"Error in PropertyOwnerDashboardStatsView: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)