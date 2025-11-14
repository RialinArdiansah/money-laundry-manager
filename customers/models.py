from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class Customer(models.Model):
    """
    Customer model for storing laundry customer information.
    """
    name = models.CharField(
        max_length=100,
        help_text="Full name of the customer"
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Customer address"
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        help_text="Phone number for contact"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email address for notifications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this customer is active"
    )

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

    def get_total_orders(self):
        """Return total number of orders for this customer"""
        return self.orders.count()

    def get_pending_orders(self):
        """Return number of pending orders"""
        return self.orders.filter(status__in=['Diterima', 'Proses']).count()

    def get_last_order_date(self):
        """Return date of last order"""
        last_order = self.order_set.order_by('-created_at').first()
        return last_order.created_at if last_order else None
