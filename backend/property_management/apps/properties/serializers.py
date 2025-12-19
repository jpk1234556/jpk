from rest_framework import serializers
from .models import Property
from apps.users.models import User


class PropertySerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    total_units = serializers.IntegerField(read_only=True)
    occupied_units = serializers.IntegerField(read_only=True)
    occupancy_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'name', 'type', 'address', 'owner', 'owner_name',
            'total_units', 'occupied_units', 'occupancy_rate',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_occupancy_rate(self, obj):
        """Calculate occupancy rate percentage"""
        total = getattr(obj, 'total_units', 0)
        occupied = getattr(obj, 'occupied_units', 0)
        if total == 0:
            return 0
        return round((occupied / total) * 100, 2)


class PropertyDetailSerializer(PropertySerializer):
    """Extended serializer for detailed property view"""
    units = serializers.SerializerMethodField()
    recent_maintenance = serializers.SerializerMethodField()
    monthly_revenue = serializers.SerializerMethodField()
    
    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields + [
            'units', 'recent_maintenance', 'monthly_revenue'
        ]
    
    def get_units(self, obj):
        """Get basic unit information"""
        from apps.units.serializers import UnitSerializer
        return UnitSerializer(obj.units.all()[:10], many=True).data
    
    def get_recent_maintenance(self, obj):
        """Get recent maintenance requests for this property"""
        from apps.maintenance.models import MaintenanceRequest
        recent_requests = MaintenanceRequest.objects.filter(
            unit__property=obj
        ).order_by('-created_at')[:5]
        
        return [{
            'id': req.id,
            'title': req.title,
            'status': req.status,
            'priority': req.priority,
            'created_at': req.created_at
        } for req in recent_requests]
    
    def get_monthly_revenue(self, obj):
        """Calculate monthly revenue from all units"""
        from django.db.models import Sum
        return obj.units.aggregate(
            total_revenue=Sum('price')
        )['total_revenue'] or 0


class PropertyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating properties with validation"""
    
    class Meta:
        model = Property
        fields = ['name', 'type', 'address', 'owner']
    
    def validate_owner(self, value):
        """Ensure owner is a property owner"""
        if value.role != 'property_owner':
            raise serializers.ValidationError(
                "Owner must be a user with 'property_owner' role"
            )
        if not value.is_approved:
            raise serializers.ValidationError(
                "Owner must be approved before being assigned properties"
            )
        return value
    
    def validate_name(self, value):
        """Ensure property name is unique for the owner"""
        owner = self.initial_data.get('owner')
        if owner and Property.objects.filter(name=value, owner=owner).exists():
            raise serializers.ValidationError(
                "A property with this name already exists for this owner"
            )
        return value