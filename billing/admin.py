from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "service",
        "amount",
        "status",
        "payment_status",
        "created_at",
    )