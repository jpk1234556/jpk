"""
Signals for the users app to handle automatic email notifications.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging

from .models import User
from utils.email_utils import EmailNotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_user_notification(sender, instance, created, **kwargs):
    """
    Send email notifications when users are created or approved.
    
    Args:
        sender: The model class sending the signal
        instance: The actual instance being saved
        created: Boolean indicating if a new record was created
        **kwargs: Additional keyword arguments
    """
    try:
        # Send notification to admin when new user registers
        if created:
            EmailNotificationService.send_user_registration_notification(instance)
            logger.info(f"Registration notification sent for user {instance.username}")
    except Exception as e:
        logger.error(f"Error sending registration notification: {str(e)}")


# We'll handle user approval notifications in the view since it's easier to detect changes there