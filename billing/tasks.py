from celery import shared_task
from django.utils.timezone import now
from django.db import transaction
from datetime import timedelta

from providers.models import CustomerAccount
from billing.models import Bill, BillStatus, PaymentStatus


@shared_task
def generate_monthly_invoices():
    today = now().date()
    created_count = 0

    accounts = CustomerAccount.objects.select_related("user", "service")

    for acc in accounts:
        with transaction.atomic():   # ✅ ensures safe DB operation

            # get latest bill
            last_bill = (
                Bill.objects
                .filter(user=acc.user, service=acc.service)
                .order_by("-created_at")
                .first()
            )

            
            if last_bill and last_bill.payment_status  != PaymentStatus.SUCCESS:
                continue
            

        
            

            
            Bill.objects.create(
                user=acc.user,
                service=acc.service,
                account_number=acc.account_number,
                amount=acc.service.price,   # 👈 direct from service
                status=BillStatus.UNPAID,
                payment_status=PaymentStatus.PENDING,
                due_date=today + timedelta(days=15)
            )

            created_count += 1

    return f"{created_count} bills created"