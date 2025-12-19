from rest_framework import generics, permissions
from rest_framework.response import Response
import logging
from apps.users.models import User
from apps.properties.models import Property
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Count
from apps.tenants.models import Tenant

# Set up logging
logger = logging.getLogger(__name__)


class AdminDashboardStatsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Check if user is admin
            if hasattr(request.user, 'role') and request.user.role == 'admin':
                # Create cache key based on user
                cache_key = f"admin_dashboard_stats_{request.user.id}"
                
                # Try to get data from cache first
                stats = cache.get(cache_key)
                
                if stats is None:
                    # Get statistics
                    property_owners = User.objects.filter(role='property_owner')
                    total_owners = property_owners.count()
                    pending_approvals = property_owners.filter(
                        is_approved=False).count()
                    total_properties = Property.objects.count()
                    
                    # Active tenants = tenants with an active lease today
                    today = timezone.now().date()
                    active_tenants = Tenant.objects.filter(
                        lease_start__lte=today,
                        lease_end__gte=today,
                    ).count()

                    stats = {
                        'totalOwners': total_owners,
                        'totalProperties': total_properties,
                        'pendingApprovals': pending_approvals,
                        'activeTenants': active_tenants
                    }
                    
                    # Cache for 5 minutes
                    cache.set(cache_key, stats, 300)

                return Response(stats)
            else:
                # Return forbidden for non-admin users
                return Response({'error': 'Access denied. Admin access required.'}, status=403)
        except Exception as e:
            logger.error(f"Error in AdminDashboardStatsView: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)
