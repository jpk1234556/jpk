from rest_framework import serializers
from .models import Payment
from apps.tenants.models import Tenant


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'tenant', 'amount', 'payment_date', 'payment_method', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']