from django.db import models
from django.utils import timezone
from apps.properties.models import Property


class Unit(models.Model):
    """
    Unit model representing a room or unit within a property.
    
    Each unit belongs to a property and can be rented to tenants.
    Units have a status that indicates their availability.
    """
    
    # Unit status choices
    STATUS_CHOICES = (
        ('available', 'Available'),    # Unit is ready for occupancy
        ('occupied', 'Occupied'),      # Unit is currently rented
        ('maintenance', 'Maintenance') # Unit is under maintenance
    )
    
    # The property this unit belongs to
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units', db_index=True)
    
    # Identifier for the unit (e.g., room number, apartment number)
    unit_number = models.CharField(max_length=50, db_index=True)
    
    # Type of unit (e.g., Studio, 1 Bedroom, 2 Bedroom, Private Room, Dormitory Room)
    type = models.CharField(max_length=50, db_index=True)
    
    # Maximum number of occupants for this unit
    capacity = models.IntegerField()
    
    # Monthly rent price for this unit
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    
    # Current status of the unit from the predefined choices
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', db_index=True)
    
    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    class Meta:
        indexes = [
            models.Index(fields=['property', 'status']),
            models.Index(fields=['property', 'unit_number']),
            models.Index(fields=['status', 'price']),
            models.Index(fields=['type', 'status']),
        ]
        ordering = ['property', 'unit_number']
        unique_together = ['property', 'unit_number']
    
    def __str__(self):
        """Return a string representation including property name and unit number."""
        return f"{self.property.name} - {self.unit_number}"
    
    def is_available(self):
        """Check if unit is available for rent."""
        return self.status == 'available'
    
    def is_occupied(self):
        """Check if unit is currently occupied."""
        return self.status == 'occupied'
    
    def get_current_tenant(self):
        """Get the current tenant if unit is occupied."""
        if self.is_occupied():
            return self.tenants.filter(lease_end_date__gte=timezone.now().date()).first()
        return None