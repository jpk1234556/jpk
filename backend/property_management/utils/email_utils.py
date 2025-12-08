"""
Utility module for sending email notifications in the property management system.
"""
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """
    Service class for sending various types of email notifications.
    """
    
    @staticmethod
    def _is_email_configured():
        """
        Check if email settings are properly configured.
        
        Returns:
            bool: True if email is configured, False otherwise
        """
        return (
            hasattr(settings, 'EMAIL_HOST') and 
            settings.EMAIL_HOST and 
            hasattr(settings, 'EMAIL_HOST_USER') and 
            settings.EMAIL_HOST_USER
        )
    
    @staticmethod
    def send_user_registration_notification(user):
        """
        Send notification to admin when a new user registers.
        
        Args:
            user: User object that just registered
        """
        # Check if email is configured
        if not EmailNotificationService._is_email_configured():
            logger.warning("Email not configured. Skipping user registration notification.")
            return
        
        try:
            subject = f"New User Registration: {user.username}"
            context = {
                'user': user,
                'approval_url': f"{settings.FRONTEND_BASE_URL}/admin/users/{user.id}/approve"
            }
            
            html_message = render_to_string('emails/new_user_registration.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Sent registration notification for user {user.username}")
        except Exception as e:
            logger.error(f"Failed to send registration notification for user {user.username}: {str(e)}")
    
    @staticmethod
    def send_user_approval_notification(user):
        """
        Send notification to user when their account is approved.
        
        Args:
            user: User object whose account was approved
        """
        # Check if email is configured
        if not EmailNotificationService._is_email_configured():
            logger.warning("Email not configured. Skipping user approval notification.")
            return
        
        try:
            subject = "Your Account Has Been Approved"
            context = {
                'user': user,
                'login_url': f"{settings.FRONTEND_BASE_URL}/login"
            }
            
            html_message = render_to_string('emails/user_approved.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Sent approval notification to user {user.username}")
        except Exception as e:
            logger.error(f"Failed to send approval notification to user {user.username}: {str(e)}")
    
    @staticmethod
    def send_rent_due_notification(tenant, amount, due_date):
        """
        Send rent due notification to tenant.
        
        Args:
            tenant: Tenant object
            amount: Rent amount due
            due_date: Date when rent is due
        """
        # Check if email is configured
        if not EmailNotificationService._is_email_configured():
            logger.warning("Email not configured. Skipping rent due notification.")
            return
        
        # Check if tenant has email
        if not tenant.email:
            logger.warning(f"Tenant {tenant.full_name} has no email address. Skipping rent due notification.")
            return
        
        try:
            subject = f"Rent Due Notice - ${amount} Due by {due_date.strftime('%B %d, %Y')}"
            context = {
                'tenant': tenant,
                'amount': amount,
                'due_date': due_date,
                'payment_url': f"{settings.FRONTEND_BASE_URL}/tenant/payments"
            }
            
            html_message = render_to_string('emails/rent_due.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[tenant.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Sent rent due notification to tenant {tenant.full_name}")
        except Exception as e:
            logger.error(f"Failed to send rent due notification to tenant {tenant.full_name}: {str(e)}")
    
    @staticmethod
    def send_maintenance_request_notification(maintenance_request, property_manager_email):
        """
        Send maintenance request notification to property manager.
        
        Args:
            maintenance_request: MaintenanceRequest object
            property_manager_email: Email address of property manager
        """
        # Check if email is configured
        if not EmailNotificationService._is_email_configured():
            logger.warning("Email not configured. Skipping maintenance request notification.")
            return
        
        try:
            subject = f"Maintenance Request: {maintenance_request.title}"
            context = {
                'request': maintenance_request,
                'view_url': f"{settings.FRONTEND_BASE_URL}/admin/maintenance/{maintenance_request.id}"
            }
            
            html_message = render_to_string('emails/maintenance_request.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[property_manager_email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Sent maintenance request notification for request {maintenance_request.id}")
        except Exception as e:
            logger.error(f"Failed to send maintenance request notification: {str(e)}")
    
    @staticmethod
    def send_payment_received_notification(tenant, amount, payment_date):
        """
        Send payment received notification to tenant.
        
        Args:
            tenant: Tenant object
            amount: Payment amount received
            payment_date: Date when payment was received
        """
        # Check if email is configured
        if not EmailNotificationService._is_email_configured():
            logger.warning("Email not configured. Skipping payment received notification.")
            return
        
        # Check if tenant has email
        if not tenant.email:
            logger.warning(f"Tenant {tenant.full_name} has no email address. Skipping payment received notification.")
            return
        
        try:
            subject = f"Payment Received - ${amount} on {payment_date.strftime('%B %d, %Y')}"
            context = {
                'tenant': tenant,
                'amount': amount,
                'payment_date': payment_date,
                'receipt_url': f"{settings.FRONTEND_BASE_URL}/tenant/receipts/{payment_date.strftime('%Y%m%d')}"
            }
            
            html_message = render_to_string('emails/payment_received.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[tenant.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Sent payment received notification to tenant {tenant.full_name}")
        except Exception as e:
            logger.error(f"Failed to send payment received notification to tenant {tenant.full_name}: {str(e)}")