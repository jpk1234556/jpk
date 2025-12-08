from rest_framework import serializers
from .models import Property
from apps.users.models import User


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'name', 'type', 'address', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']