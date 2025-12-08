from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'is_approved']
        read_only_fields = ['id', 'role', 'is_approved']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Force role to property_owner and is_approved to False for new registrations
        user = User.objects.create(
            role='property_owner',
            is_approved=False,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user