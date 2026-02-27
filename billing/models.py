from django.db import models
from hospital.models import Appointment

class Invoice(models.Model):
    class Status(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PAID = 'PAID', 'Paid'
        CANCELLED = 'CANCELLED', 'Cancelled'

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='invoice')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID)
    issued_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.amount + self.tax
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.id} for {self.appointment}"
