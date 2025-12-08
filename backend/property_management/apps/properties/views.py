from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


class IsPropertyOwner(permissions.BasePermission):
    """
    Custom permission to only allow property owners to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'property_owner'


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
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
        user = self.request.user
        if user.role == 'admin':
            return Property.objects.all()
        elif user.role == 'property_owner':
            return Property.objects.filter(owner=user)
        return Property.objects.none()


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

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
        user = self.request.user
        if user.role == 'admin':
            return Property.objects.all()
        elif user.role == 'property_owner':
            return Property.objects.filter(owner=user)
        return Property.objects.none()