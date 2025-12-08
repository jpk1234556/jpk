from rest_framework import generics, permissions
from .models import MaintenanceRequest
from .serializers import MaintenanceRequestSerializer


class MaintenanceRequestListCreateView(generics.ListCreateAPIView):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return MaintenanceRequest.objects.select_related('unit', 'submitted_by', 'assigned_to').all()
        elif user.role == 'property_owner':
            return MaintenanceRequest.objects.select_related('unit', 'submitted_by', 'assigned_to').filter(unit__property__owner=user)
        return MaintenanceRequest.objects.none()


class MaintenanceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return MaintenanceRequest.objects.select_related('unit', 'submitted_by', 'assigned_to').all()
        elif user.role == 'property_owner':
            return MaintenanceRequest.objects.select_related('unit', 'submitted_by', 'assigned_to').filter(unit__property__owner=user)
        return MaintenanceRequest.objects.none()