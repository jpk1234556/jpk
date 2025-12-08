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
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Approval status - users must be approved by admin before accessing the system
    is_approved = models.BooleanField(default=False)
    
    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    def __str__(self):
        """Return the username as the string representation of the user."""
        return self.username