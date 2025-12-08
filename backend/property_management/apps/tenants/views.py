from rest_framework import generics, permissions
from .models import Tenant
from .serializers import TenantSerializer


class TenantListCreateView(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Tenant.objects.select_related('unit').all()
        elif user.role == 'property_owner':
            return Tenant.objects.select_related('unit').filter(unit__property__owner=user)
        return Tenant.objects.none()


class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Tenant.objects.select_related('unit').all()
        elif user.role == 'property_owner':
            return Tenant.objects.select_related('unit').filter(unit__property__owner=user)
        return Tenant.objects.none()