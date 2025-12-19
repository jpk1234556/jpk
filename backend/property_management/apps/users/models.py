from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    This model adds role-based access control and approval functionality
    to the standard Django user model.
    """
    
    # Role choices for user permissions
    ROLE_CHOICES = (
        ('admin', 'Admin'),                    # System administrator with full access
        ('property_owner', 'Property Owner')   # Property owner with limited access
    )
    
    # Email must be unique for each user
    email = models.EmailField(unique=True)
    
    # User role determines access permissions
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)
    
    # Approval status - users must be approved by admin before accessing the system
    is_approved = models.BooleanField(default=False, db_index=True)
    
    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    class Meta:
        indexes = [
            models.Index(fields=['role', 'is_approved']),
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        """Return the username as the string representation of the user."""
        return self.username
    
    @property
    def is_admin(self):
        """Check if user is an admin."""
        return self.role == 'admin'
    
    @property
    def is_property_owner(self):
        """Check if user is a property owner."""
        return self.role == 'property_owner'