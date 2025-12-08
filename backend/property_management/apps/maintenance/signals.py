"""
Signals for the maintenance app to handle automatic email notifications.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from .models import MaintenanceRequest
from utils.email_utils import EmailNotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=MaintenanceRequest)
def send_maintenance_notification(sender, instance, created, **kwargs):
    """
    Send email notifications when maintenance requests are created.
    
    Args:
        sender: The model class sending the signal
        instance: The actual instance being saved
        created: Boolean indicating if a new record was created
        **kwargs: Additional keyword arguments
    """
    try:
        # Send notification to property manager when new maintenance request is created
        if created:
            # In a real application, you would determine the property manager based on the unit
            # For now, we'll use the admin email from settings
            from django.conf import settings
            property_manager_email = getattr(settings, 'ADMIN_EMAIL', 'admin@propertymanagement.com')
            
            EmailNotificationService.send_maintenance_request_notification(instance, property_manager_email)
            logger.info(f"Maintenance request notification sent for request {instance.id}")
    except Exception as e:
        logger.error(f"Error sending maintenance request notification: {str(e)}")