from django.db import models
from apps.users.models import User


class Property(models.Model):
    """
    Property model representing a real estate property managed in the system.
    
    Each property is owned by a user with the 'property_owner' role and can
    contain multiple units/rooms.
    """
    
    # Property type choices
    TYPE_CHOICES = (
        ('hostel', 'Hostel'),      # Shared accommodation with multiple rooms
        ('apartment', 'Apartment'), # Self-contained housing unit
        ('hotel', 'Hotel'),         # Commercial lodging establishment
        ('rental', 'Rental')        # General rental property
    )
    
    # Property name/description
    name = models.CharField(max_length=100, db_index=True)
    
    # Property type from the predefined choices
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, db_index=True)
    
    # Physical address of the property (optional)
    address = models.TextField(blank=True)
    
    # Owner of the property (must be a user with role='property_owner')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', db_index=True)
    
    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    class Meta:
        """Model metadata options."""
        verbose_name_plural = "Properties"
        indexes = [
            models.Index(fields=['owner', 'type']),
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        """Return the property name as the string representation."""
        return self.name
    
    @property
    def total_units(self):
        """Get total number of units in this property."""
        return self.units.count()
    
    @property
    def occupied_units(self):
        """Get number of occupied units in this property."""
        return self.units.filter(status='occupied').count()
    
    @property
    def occupancy_rate(self):
        """Calculate occupancy rate as a percentage."""
        total = self.total_units
        if total == 0:
            return 0
        return (self.occupied_units / total) * 100