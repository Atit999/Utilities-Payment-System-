

from django.db import models
from django.conf import settings
from billing.models import Bill


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"


class PaymentMethod(models.TextChoices):
    KHALTI = "KHALTI", "Khalti"
    ESEWA = "ESEWA", "eSewa"
    


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE)

    method = models.CharField(max_length=20, choices=PaymentMethod.choices)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    initial_id = models.CharField(max_length=200, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    txn_id = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"
