from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from customers.models import Customer
import uuid

def generate_order_number():
    """Generate unique order number with format ML-YYYYMMDD-XXXX"""
    today = timezone.now().strftime("%Y%m%d")
    random_num = str(uuid.uuid4()).split('-')[0].upper()[:4]
    return f"ML-{today}-{random_num}"

class Order(models.Model):
    """
    Order model for managing laundry orders.
    """
    SERVICE_TYPE_CHOICES = [
        ('express', 'Express (1 hari)'),
        ('regular', 'Regular (3 hari)'),
    ]

    STATUS_CHOICES = [
        ('diterima', 'Diterima'),
        ('proses', 'Proses'),
        ('selesai', 'Selesai'),
        ('diambil', 'Siap Diambil/Diambil'),
    ]

    order_number = models.CharField(
        max_length=20,
        unique=True,
        default=generate_order_number,
        editable=False,
        help_text="Unique order number"
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="Customer who placed the order"
    )
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_TYPE_CHOICES,
        default='regular',
        help_text="Type of service: Express or Regular"
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        help_text="Weight of laundry in kg"
    )
    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text="Price per kg for the selected service"
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        help_text="Total cost calculated automatically"
    )
    date_received = models.DateField(
        default=timezone.now,
        help_text="Date when laundry was received"
    )
    estimated_completion = models.DateField(
        help_text="Estimated completion date based on service type"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='diterima',
        help_text="Current status of the order"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the order"
    )
    storage_deadline = models.DateField(
        blank=True,
        null=True,
        help_text="Deadline for customer to pick up completed laundry"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_orders',
        help_text="Employee who created this order"
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['date_received']),
            models.Index(fields=['estimated_completion']),
        ]

    def __str__(self):
        return f"{self.order_number} - {self.customer.name}"

    def save(self, *args, **kwargs):
        # Set unit price based on service type if not provided
        if not self.unit_price:
            self.unit_price = self.get_service_price()

        # Calculate total cost
        self.total_cost = self.weight * self.unit_price

        # Set estimated completion date based on service type
        if not self.estimated_completion:
            self.set_estimated_completion()

        super().save(*args, **kwargs)

    def get_service_price(self):
        """Get price per kg based on service type"""
        prices = {
            'express': 15000,  # Rp 15,000/kg for express
            'regular': 10000,  # Rp 10,000/kg for regular
        }
        return prices.get(self.service_type, 10000)

    def set_estimated_completion(self):
        """Set estimated completion date based on service type"""
        from datetime import timedelta

        days_map = {
            'express': 1,  # 1 day for express
            'regular': 3,  # 3 days for regular
        }

        days = days_map.get(self.service_type, 3)
        self.estimated_completion = self.date_received + timedelta(days=days)

        # Set storage deadline (7 days after completion)
        if self.status == 'selesai':
            self.storage_deadline = self.estimated_completion + timedelta(days=7)

    def is_overdue(self):
        """Check if order is overdue"""
        if self.status in ['selesai', 'diambil']:
            return False
        return timezone.now().date() > self.estimated_completion

    def days_in_storage(self):
        """Calculate days in storage if completed but not picked up"""
        if self.status == 'selesai' and self.storage_deadline:
            return (timezone.now().date() - self.estimated_completion).days
        return 0

    def get_status_display_with_color(self):
        """Return status display with color class for frontend"""
        color_map = {
            'diterima': 'warning',
            'proses': 'info',
            'selesai': 'success',
            'diambil': 'secondary'
        }
        return {
            'status': self.get_status_display(),
            'color': color_map.get(self.status, 'primary')
        }
