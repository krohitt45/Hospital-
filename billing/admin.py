from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'total_amount', 'status', 'issued_date')
    list_filter = ('status', 'issued_date')
    readonly_fields = ('total_amount', 'issued_date')
