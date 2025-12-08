from rest_framework import serializers
from .models import MaintenanceRequest
from apps.units.models import Unit
from apps.users.models import User


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'unit', 'submitted_by', 'title', 'description', 'priority', 'status', 'assigned_to', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
