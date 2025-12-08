from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.select_related('tenant').all()
        elif user.role == 'property_owner':
            return Payment.objects.select_related('tenant').filter(tenant__unit__property__owner=user)
        return Payment.objects.none()


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.select_related('tenant').all()
        elif user.role == 'property_owner':
            return Payment.objects.select_related('tenant').filter(tenant__unit__property__owner=user)
        return Payment.objects.none()