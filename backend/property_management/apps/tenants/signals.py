"""
Signals for the tenants app to handle automatic email notifications.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from datetime import date, timedelta
import logging

from .models import Tenant
from utils.email_utils import EmailNotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Tenant)
def send_rent_due_notification(sender, instance, created, **kwargs):
    """
    Send email notifications when rent is due based on lease information.
    
    Args:
        sender: The model class sending the signal
        instance: The actual instance being saved
        created: Boolean indicating if a new record was created
        **kwargs: Additional keyword arguments
    """
    try:
        # Send notification when a tenant is created or updated
        # In a real application, this would be triggered by a scheduled task
        # that checks for upcoming rent due dates
        
        # For demonstration purposes, we'll just log that the tenant exists
        # A real implementation would have a scheduled job that runs daily
        # to check for tenants with rent due soon
        
        if created:
            logger.info(f"Tenant {instance.full_name} added with lease start {instance.lease_start}")
            
    except Exception as e:
        logger.error(f"Error in tenant notification signal: {str(e)}")


def check_rent_due_notifications():
    """
    Function to check for upcoming rent due dates and send notifications.
    This would typically be called by a scheduled task (cron job or Celery beat).
    """
    try:
        # Get all active tenants (lease hasn't ended)
        today = date.today()
        active_tenants = Tenant.objects.filter(lease_end__gte=today)
        
        # For each active tenant, check if rent is due soon
        # In a real implementation, you'd want to track the last notification date
        # to avoid sending duplicate notifications
        
        for tenant in active_tenants:
            # Calculate days until lease end
            days_until_end = (tenant.lease_end - today).days
            
            # Send notification if lease is ending soon (e.g., within 30 days)
            if days_until_end <= 30:
                # Send lease expiry notification
                logger.info(f"Sending lease expiry notification to {tenant.full_name}")
                
    except Exception as e:
        logger.error(f"Error checking rent due notifications: {str(e)}")