from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending AbstractUser to support role-based access control.
    Handles both Pegawai (Employee) and Owner roles.
    """
    ROLE_CHOICES = [
        ('pegawai', 'Pegawai'),
        ('owner', 'Owner'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='pegawai',
        help_text="User role: Pegawai or Owner"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Phone number for contact"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_pegawai(self):
        return self.role == 'pegawai'

    def is_owner(self):
        return self.role == 'owner'
