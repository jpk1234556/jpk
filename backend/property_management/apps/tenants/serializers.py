from rest_framework import serializers
from .models import Tenant
from apps.units.models import Unit


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'unit', 'lease_start', 'lease_end', 'rent_amount', 'deposit_amount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']