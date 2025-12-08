from rest_framework import generics, permissions
from .models import Unit
from .serializers import UnitSerializer


class UnitListCreateView(generics.ListCreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Unit.objects.select_related('property').all()
        elif user.role == 'property_owner':
            return Unit.objects.select_related('property').filter(property__owner=user)
        return Unit.objects.none()


class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Unit.objects.select_related('property').all()
        elif user.role == 'property_owner':
            return Unit.objects.select_related('property').filter(property__owner=user)
        return Unit.objects.none()