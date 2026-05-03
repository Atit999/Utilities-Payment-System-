from django.db import models

from django.db import models
from django.conf import settings


class Provider(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)  # NEA, NTC

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='services'
    )

    name = models.CharField(max_length=100)  # Electricity, Prepaid, etc.
    code = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.name} - {self.name}"


class CustomerAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    account_number = models.CharField(max_length=100)  # meter no / phone no
    nickname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user} - {self.account_number}"


# Create your models here.
