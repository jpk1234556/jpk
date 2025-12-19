from django.db import models
from apps.units.models import Unit
from apps.users.models import User


class MaintenanceRequest(models.Model):
    """
    MaintenanceRequest model representing a maintenance issue reported for a unit.
    
    Tenants or property owners can submit maintenance requests which can be
    tracked through different statuses and priorities.
    """
    
    # Priority levels for maintenance requests
    PRIORITY_CHOICES = (
        ('low', 'Low'),          # Minor issues that can wait
        ('medium', 'Medium'),    # Standard issues requiring attention
        ('high', 'High'),        # Important issues needing prompt attention
        ('urgent', 'Urgent')     # Critical issues requiring immediate attention
    )
    
    # Status options for tracking maintenance progress
    STATUS_CHOICES = (
        ('pending', 'Pending'),           # Request submitted but not yet addressed
        ('in_progress', 'In Progress'),   # Work has started on the request
        ('completed', 'Completed'),       # Request has been fulfilled
        ('cancelled', 'Cancelled')        # Request was cancelled
    )
    
    # The unit this maintenance request is for
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='maintenance_requests')
    
    # The user who submitted this request (can be tenant or property owner)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_requests')
    
    # Brief title describing the maintenance issue
    title = models.CharField(max_length=100)
    
    # Detailed description of the maintenance issue
    description = models.TextField()
    
    # Priority level of the request from the predefined choices
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Current status of the request from the predefined choices
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # User assigned to work on this request (optional)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    
    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    def __str__(self):
        """Return the maintenance request title as the string representation."""
        return self.title
    
    class Meta:
        """Model metadata options."""
        ordering = ['-created_at']  # Order by creation date, newest first
        indexes = [
            models.Index(fields=['unit']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
            models.Index(fields=['unit', 'status']),
        ]