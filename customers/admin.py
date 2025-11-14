from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'is_active', 'created_at', 'get_total_orders')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'phone_number', 'email')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'get_total_orders', 'get_pending_orders')

    fieldsets = (
        (None, {
            'fields': ('name', 'phone_number', 'email', 'address')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('get_total_orders', 'get_pending_orders'),
            'classes': ('collapse',)
        }),
    )

    def get_total_orders(self, obj):
        return obj.get_total_orders()
    get_total_orders.short_description = 'Total Orders'

    def get_pending_orders(self, obj):
        return obj.get_pending_orders()
    get_pending_orders.short_description = 'Pending Orders'
