from rest_framework import serializers
from .models import Unit
from apps.properties.models import Property


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'property', 'unit_number', 'type', 'capacity', 'price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
