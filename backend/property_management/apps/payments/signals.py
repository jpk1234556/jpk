"""
Signals for the payments app to handle automatic email notifications.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from .models import Payment
from utils.email_utils import EmailNotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Payment)
def send_payment_notification(sender, instance, created, **kwargs):
    """
    Send email notifications when payments are received.
    
    Args:
        sender: The model class sending the signal
        instance: The actual instance being saved
        created: Boolean indicating if a new record was created
        **kwargs: Additional keyword arguments
    """
    try:
        # Send notification to tenant when payment is recorded
        if created:
            EmailNotificationService.send_payment_received_notification(
                instance.tenant, 
                float(instance.amount), 
                instance.payment_date
            )
            logger.info(f"Payment received notification sent for payment {instance.id}")
    except Exception as e:
        logger.error(f"Error sending payment received notification: {str(e)}")