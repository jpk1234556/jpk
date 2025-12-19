from django.db import models
from apps.tenants.models import Tenant


class Payment(models.Model):
    """
    Payment model representing a payment made by a tenant.
    
    Each payment is associated with a specific tenant and includes details
    about the amount, date, and payment method.
    """
    
    # Available payment methods
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),                    # Physical cash payment
        ('check', 'Check'),                  # Check payment
        ('credit_card', 'Credit Card'),      # Credit card payment
        ('bank_transfer', 'Bank Transfer'),  # Electronic bank transfer
        ('other', 'Other')                   # Other payment methods
    )
    
    # The tenant who made this payment
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    
    # Payment amount in the system's currency
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Date when the payment was made
    payment_date = models.DateField()
    
    # Method used for this payment from the predefined choices
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True)
    
    # Optional description or notes about the payment
    description = models.TextField(blank=True)
    
    # Timestamp for when this payment record was created
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    
    def __str__(self):
        """Return a string representation including amount and tenant name."""
        return f"Payment of ${self.amount} from {self.tenant.full_name}"
    
    class Meta:
        """Model metadata options."""
        ordering = ['-payment_date']  # Order by payment date, newest first
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['payment_date']),
        ]