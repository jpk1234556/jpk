"""
Management command to send rent due notifications to tenants.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import date, timedelta
import logging

from apps.tenants.models import Tenant
from utils.email_utils import EmailNotificationService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send rent due notifications to tenants'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days-before-due',
            type=int,
            default=5,
            help='Number of days before rent is due to send notification (default: 5)'
        )
    
    def handle(self, *args, **options):
        days_before_due = options['days_before_due']
        self.stdout.write(
            self.style.SUCCESS(f'Sending rent due notifications for tenants with rent due in {days_before_due} days')
        )
        
        try:
            # Calculate the target date for notifications
            target_date = date.today() + timedelta(days=days_before_due)
            
            # In a real implementation, you would have a way to track rent due dates
            # For this example, we'll assume rent is due on the 1st of each month
            # and send notifications to all tenants
            
            # Get all active tenants
            today = date.today()
            active_tenants = Tenant.objects.filter(lease_end__gte=today)
            
            notification_count = 0
            
            for tenant in active_tenants:
                try:
                    # Send rent due notification
                    # In a real implementation, you would calculate the actual due date
                    # and amount based on the tenant's lease agreement
                    EmailNotificationService.send_rent_due_notification(
                        tenant, 
                        float(tenant.rent_amount), 
                        target_date
                    )
                    notification_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Sent notification to {tenant.full_name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to send notification to {tenant.full_name}: {str(e)}')
                    )
                    logger.error(f'Failed to send rent due notification to {tenant.full_name}: {str(e)}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully sent {notification_count} rent due notifications')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending rent due notifications: {str(e)}')
            )
            logger.error(f'Error in send_rent_notifications command: {str(e)}')