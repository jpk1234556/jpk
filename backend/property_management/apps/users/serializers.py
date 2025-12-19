from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    property_count = serializers.IntegerField(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'is_approved', 'property_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        """Get user's full name"""
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class UserDetailSerializer(UserSerializer):
    """Extended serializer for detailed user view"""
    properties = serializers.SerializerMethodField()
    last_login_formatted = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'properties', 'last_login', 'last_login_formatted'
        ]
    
    def get_properties(self, obj):
        """Get user's properties with basic info"""
        if obj.role == 'property_owner':
            from apps.properties.serializers import PropertySerializer
            return PropertySerializer(obj.properties.all()[:5], many=True).data
        return []
    
    def get_last_login_formatted(self, obj):
        """Get formatted last login time"""
        if obj.last_login:
            return obj.last_login.strftime('%Y-%m-%d %H:%M:%S')
        return 'Never'


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'role', 'is_approved'
        ]
        read_only_fields = ['id', 'role', 'is_approved']

    def validate_username(self, value):
        """Validate username uniqueness and format"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long")
        
        return value

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        # Remove password_confirm from validated_data
        validated_data.pop('password_confirm', None)
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


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'is_approved'
        ]
        read_only_fields = ['id', 'username']  # Username cannot be changed
    
    def validate_role(self, value):
        """Validate role changes"""
        if self.instance and self.instance.role == 'admin' and value != 'admin':
            # Prevent removing admin role if it's the last admin
            admin_count = User.objects.filter(role='admin').count()
            if admin_count <= 1:
                raise serializers.ValidationError(
                    "Cannot remove admin role - at least one admin must exist"
                )
        return value