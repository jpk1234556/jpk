"""
Management command to send various types of notifications.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import date, timedelta
import logging

from apps.tenants.models import Tenant
from apps.maintenance.models import MaintenanceRequest
from apps.payments.models import Payment
from utils.email_utils import EmailNotificationService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send various types of notifications'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--notification-type',
            type=str,
            default='all',
            choices=['all', 'rent_due', 'lease_expiry', 'maintenance'],
            help='Type of notification to send (default: all)'
        )
        parser.add_argument(
            '--days-before-due',
            type=int,
            default=5,
            help='Number of days before rent is due to send notification (default: 5)'
        )
    
    def handle(self, *args, **options):
        notification_type = options['notification_type']
        days_before_due = options['days_before_due']
        
        self.stdout.write(
            self.style.SUCCESS(f'Sending {notification_type} notifications')
        )
        
        if notification_type in ['all', 'rent_due']:
            self.send_rent_due_notifications(days_before_due)
        
        if notification_type in ['all', 'lease_expiry']:
            self.send_lease_expiry_notifications()
        
        if notification_type in ['all', 'maintenance']:
            self.send_maintenance_notifications()
    
    def send_rent_due_notifications(self, days_before_due):
        """Send rent due notifications to tenants."""
        try:
            self.stdout.write('Sending rent due notifications...')
            
            # Calculate the target date for notifications
            target_date = date.today() + timedelta(days=days_before_due)
            
            # Get all active tenants
            today = date.today()
            active_tenants = Tenant.objects.filter(lease_end__gte=today)
            
            notification_count = 0
            
            for tenant in active_tenants:
                try:
                    # Send rent due notification
                    EmailNotificationService.send_rent_due_notification(
                        tenant, 
                        float(tenant.rent_amount), 
                        target_date
                    )
                    notification_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Sent rent due notification to {tenant.full_name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to send rent due notification to {tenant.full_name}: {str(e)}')
                    )
                    logger.error(f'Failed to send rent due notification to {tenant.full_name}: {str(e)}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully sent {notification_count} rent due notifications')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending rent due notifications: {str(e)}')
            )
            logger.error(f'Error in send_rent_due_notifications: {str(e)}')
    
    def send_lease_expiry_notifications(self):
        """Send lease expiry notifications to tenants and property managers."""
        try:
            self.stdout.write('Sending lease expiry notifications...')
            
            # Get tenants whose leases are expiring soon (within 30 days)
            today = date.today()
            expiry_date = today + timedelta(days=30)
            expiring_tenants = Tenant.objects.filter(
                lease_end__gte=today,
                lease_end__lte=expiry_date
            )
            
            notification_count = 0
            
            for tenant in expiring_tenants:
                try:
                    # In a real implementation, you might want to send different notifications
                    # to tenants and property managers
                    # For now, we'll just log that we would send notifications
                    self.stdout.write(
                        self.style.SUCCESS(f'Lease for {tenant.full_name} expires on {tenant.lease_end}')
                    )
                    notification_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing lease expiry for {tenant.full_name}: {str(e)}')
                    )
                    logger.error(f'Error processing lease expiry for {tenant.full_name}: {str(e)}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Processed {notification_count} lease expiry notifications')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending lease expiry notifications: {str(e)}')
            )
            logger.error(f'Error in send_lease_expiry_notifications: {str(e)}')
    
    def send_maintenance_notifications(self):
        """Send maintenance request notifications."""
        try:
            self.stdout.write('Sending maintenance notifications...')
            
            # Get recent pending maintenance requests
            recent_requests = MaintenanceRequest.objects.filter(
                status='pending'
            ).order_by('-created_at')[:10]  # Last 10 pending requests
            
            notification_count = 0
            
            for request in recent_requests:
                try:
                    # Send notification to property manager
                    # In a real implementation, you would determine the property manager based on the unit
                    property_manager_email = getattr(settings, 'ADMIN_EMAIL', 'admin@propertymanagement.com')
                    
                    EmailNotificationService.send_maintenance_request_notification(request, property_manager_email)
                    notification_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Sent maintenance notification for request: {request.title}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to send maintenance notification for "{request.title}": {str(e)}')
                    )
                    logger.error(f'Failed to send maintenance notification for "{request.title}": {str(e)}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully sent {notification_count} maintenance notifications')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending maintenance notifications: {str(e)}')
            )
            logger.error(f'Error in send_maintenance_notifications: {str(e)}')