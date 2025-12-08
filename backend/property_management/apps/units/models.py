from django.db import models
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
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    
    # Identifier for the unit (e.g., room number, apartment number)
    unit_number = models.CharField(max_length=50)
    
    # Type of unit (e.g., Studio, 1 Bedroom, 2 Bedroom, Private Room, Dormitory Room)
    type = models.CharField(max_length=50)
    
    # Maximum number of occupants for this unit
    capacity = models.IntegerField()
    
    # Monthly rent price for this unit
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Current status of the unit from the predefined choices
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    def __str__(self):
        """Return a string representation including property name and unit number."""
        return f"{self.property.name} - {self.unit_number}"