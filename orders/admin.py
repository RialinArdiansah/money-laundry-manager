from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'service_type', 'weight', 'total_cost', 'status', 'date_received', 'estimated_completion', 'is_overdue')
    list_filter = ('status', 'service_type', 'date_received', 'estimated_completion', 'created_at')
    search_fields = ('order_number', 'customer__name', 'customer__phone_number', 'notes')
    ordering = ('-created_at',)
    readonly_fields = ('order_number', 'total_cost', 'created_at', 'updated_at', 'is_overdue', 'days_in_storage')

    fieldsets = (
        (None, {
            'fields': ('order_number', 'customer', 'created_by')
        }),
        ('Order Details', {
            'fields': ('service_type', 'weight', 'unit_price', 'total_cost')
        }),
        ('Dates', {
            'fields': ('date_received', 'estimated_completion', 'storage_deadline')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Order Analysis', {
            'fields': ('is_overdue', 'days_in_storage'),
            'classes': ('collapse',)
        }),
    )

    def is_overdue(self, obj):
        return obj.is_overdue()
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue?'

    def days_in_storage(self, obj):
        return obj.days_in_storage()
    days_in_storage.short_description = 'Days in Storage'
