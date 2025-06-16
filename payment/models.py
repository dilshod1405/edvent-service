from django.db import models
from authentication.models import User
from education.models import Module, Tariff, FoundationCourse

class Transaction(models.Model):
    PAYMENT_TYPE = (
        ('payme', 'Payme'),
        ('click', 'Click'),
    )

    STATE_CHOICES = (
        ('created', 'Created'),
        ('waiting', 'Waiting'),
        ('paid', 'Paid'),
        ('canceled', 'Canceled'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(FoundationCourse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Foundation Course')
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Amount (in UZS)')

    # REQUIRED by Payme-PKG
    payme_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='created')

    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.course:
            return f"{self.user} - {self.course.title}"
        if self.module:
            return f"{self.user} - {self.module.title}"
        if self.tariff:
            return f"{self.user} - {self.tariff.title}"
        return f"{self.user} - Unknown Item"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'