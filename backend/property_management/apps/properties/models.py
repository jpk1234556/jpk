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
    name = models.CharField(max_length=100)
    
    # Property type from the predefined choices
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Physical address of the property (optional)
    address = models.TextField(blank=True)
    
    # Owner of the property (must be a user with role='property_owner')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    
    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    def __str__(self):
        """Return the property name as the string representation."""
        return self.name
    
    class Meta:
        """Model metadata options."""
        verbose_name_plural = "Properties"