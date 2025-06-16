from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'module', 'tariff', 'amount', 'payme_transaction_id', 'state', 'payment_type', 'created_at', 'updated_at', 'id')
    search_fields = ('user', 'course', 'module', 'tariff', 'amount', 'payme_transaction_id', 'state', 'payment_type', 'created_at', 'updated_at')
    ordering = ('-created_at', '-updated_at', '-id')
    list_filter = ('state', 'payment_type', 'created_at', 'updated_at')