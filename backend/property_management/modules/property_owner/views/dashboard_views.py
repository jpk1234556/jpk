from rest_framework import generics, permissions
from rest_framework.response import Response
import logging
from apps.properties.models import Property
from django.core.cache import cache

# Set up logging
logger = logging.getLogger(__name__)


class PropertyOwnerDashboardStatsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        from apps.units.models import Unit
        from apps.maintenance.models import MaintenanceRequest
        
        try:
            # Check if user is property owner
            if hasattr(request.user, 'role') and request.user.role == 'property_owner':
                # Create cache key based on user
                cache_key = f"property_owner_dashboard_stats_{request.user.id}"
                
                # Try to get data from cache first
                stats = cache.get(cache_key)
                
                if stats is None:
                    # Get properties owned by this user
                    properties = Property.objects.filter(owner=request.user)
                    my_properties = properties.count()

                    # Units statistics for this owner
                    total_units = Unit.objects.filter(property__owner=request.user).count()
                    occupied_units = Unit.objects.filter(
                        property__owner=request.user,
                        status='occupied',
                    ).count()

                    # Pending maintenance requests for this owner's properties
                    pending_requests = MaintenanceRequest.objects.filter(
                        unit__property__owner=request.user,
                        status='pending',
                    ).count()

                    stats = {
                        'myProperties': my_properties,
                        'totalUnits': total_units,
                        'occupiedUnits': occupied_units,
                        'pendingRequests': pending_requests,
                    }
                    
                    # Cache for 5 minutes
                    cache.set(cache_key, stats, 300)

                return Response(stats)
            else:
                # Return forbidden for non-property owner users
                return Response({'error': 'Access denied. Property owner access required.'}, status=403)
        except Exception as e:
            logger.error(f"Error in PropertyOwnerDashboardStatsView: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)
