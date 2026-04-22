# billing/models.py

from django.db import models
from accounts.models import User
from providers.models import Service


class BillStatus(models.TextChoices):
    UNPAID = "unpaid", "Unpaid"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    account_number = models.CharField(max_length=100, blank=True)

    
    billing_month = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=10,
        choices=BillStatus.choices,
        default=BillStatus.UNPAID
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ✅ Prevent duplicate monthly invoices
        unique_together = ("user", "service", "billing_month")

    def __str__(self):
        return f"{self.user.email} - {self.service} - {self.billing_month}"