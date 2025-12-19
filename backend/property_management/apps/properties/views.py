from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q, Prefetch
from django.core.cache import cache
from .models import Property
from .serializers import PropertySerializer, PropertyDetailSerializer
import logging

logger = logging.getLogger(__name__)


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsPropertyOwner(permissions.BasePermission):
    """
    Custom permission to only allow property owners to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'property_owner'


class PropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'POST':
            # Only admin users can create properties
            return [permissions.IsAuthenticated(), IsAdminUser()]
        else:
            # Both admin and property owners can list properties, but with different filters
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Optimized queryset with prefetch_related for better performance
        """
        user = self.request.user
        
        # Base queryset with optimizations
        queryset = Property.objects.select_related('owner').prefetch_related(
            Prefetch('units', queryset=Property.objects.none())  # Avoid N+1 queries
        )
        
        # Apply filters based on user role
        if user.role == 'admin':
            queryset = queryset.all()
        elif user.role == 'property_owner':
            queryset = queryset.filter(owner=user)
        else:
            return Property.objects.none()
        
        # Apply search filters if provided
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(address__icontains=search)
            )
        
        # Apply type filter if provided
        property_type = self.request.query_params.get('type', None)
        if property_type:
            queryset = queryset.filter(type=property_type)
        
        return queryset.annotate(
            total_units=Count('units'),
            occupied_units=Count('units', filter=Q(units__status='occupied'))
        )

    def list(self, request, *args, **kwargs):
        """
        Enhanced list method with caching for admin users
        """
        # Cache key for admin property list
        if request.user.role == 'admin':
            cache_key = f"admin_properties_{request.GET.urlencode()}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        
        # Cache admin results for 5 minutes
        if request.user.role == 'admin':
            cache.set(cache_key, response.data, 300)
        
        return response


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertyDetailSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # Only admin users can update/delete properties
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAdminUser()]
        else:
            # Both admin and property owners can view properties
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Optimized queryset with all related data
        """
        user = self.request.user
        
        queryset = Property.objects.select_related('owner').prefetch_related(
            'units',
            'units__tenants',
            'units__maintenance_requests',
            'units__tenants__payments'
        )
        
        if user.role == 'admin':
            return queryset.all()
        elif user.role == 'property_owner':
            return queryset.filter(owner=user)
        return Property.objects.none()

    def update(self, request, *args, **kwargs):
        """
        Enhanced update with cache invalidation
        """
        response = super().update(request, *args, **kwargs)
        
        # Invalidate related caches
        cache.delete_many([
            f"admin_properties_*",
            f"property_{kwargs.get('pk')}_stats"
        ])
        
        return response