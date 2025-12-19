from django.db import models
from apps.units.models import Unit


class Tenant(models.Model):
    """
    Tenant model representing a person renting a unit.
    
    Each tenant is associated with a specific unit and has lease details
    including start/end dates and payment amounts.
    """
    
    # Tenant's first name
    first_name = models.CharField(max_length=50)
    
    # Tenant's last name
    last_name = models.CharField(max_length=50)
    
    # Tenant's email address (optional)
    email = models.EmailField(blank=True)
    
    # Tenant's phone number (optional)
    phone = models.CharField(max_length=20, blank=True)
    
    # The unit this tenant is renting
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tenants')
    
    # Start date of the lease agreement
    lease_start = models.DateField()
    
    # End date of the lease agreement
    lease_end = models.DateField()
    
    # Monthly rent amount
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Security deposit amount
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    class Meta:
        indexes = [
            models.Index(fields=['unit']),
            models.Index(fields=['lease_start', 'lease_end']),
        ]
    
    def __str__(self):
        """Return the tenant's full name as the string representation."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        """Return the tenant's full name as a property."""
        return f"{self.first_name} {self.last_name}"