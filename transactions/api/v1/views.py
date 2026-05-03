import requests
from django.conf import settings
from django.db import transaction as db_transaction

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from billing.models import Bill, BillStatus, PaymentStatus
from payments.models import Payment
from .serializers import InitiatePaymentSerializer


# -------------------------
# INITIATE KHALTI PAYMENT
# -------------------------
class InitiateKhaltiPaymentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InitiatePaymentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_verified:
            return Response(
                {"detail": "Please verify your account first"},
                status=403
            )

        bill_id = serializer.validated_data["bill_id"]

        try:
            bill = Bill.objects.get(id=bill_id, user=request.user)
        except Bill.DoesNotExist:
            return Response({"detail": "Bill not found"}, status=404)

        if bill.payment_status == PaymentStatus.SUCCESS:
            return Response({"detail": "Bill already paid"}, status=400)

        payload = {
            "return_url": "http://127.0.0.1:8000/api/khalti/callback/",
            "website_url": "http://localhost:3000/",
            "amount": int(bill.amount * 100),
            "purchase_order_id": str(bill.id),
            "purchase_order_name": "Bill Payment",
            "customer_info": {
                "name": request.user.username,
                "email": request.user.email,
                "phone": str(request.user.phone),
            },
        }

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"
        }

        response = requests.post(
            settings.KHALTI_INIT_URL,
            json=payload,
            headers=headers
        )

        data = response.json()

        # 🔥 DEBUG (important for now)
        print("KHALTI RESPONSE:", data)

        pidx = data.get("pidx")

        if not pidx:
            return Response(
                {"detail": "Failed to get pidx", "response": data},
                status=400
            )

        # ✅ SAVE PAYMENT HERE (THIS WAS MISSING)
        Payment.objects.create(
            bill=bill,
            user=request.user,
            amount=bill.amount,
            txn_id=pidx,
            status=PaymentStatus.PENDING,
            method="khalti"
        )

        print("SAVED TXN:", pidx)

        return Response(data)


# -------------------------
# KHALTI CALLBACK (VERIFY + UPDATE)
# -------------------------
class KhaltiCallbackView(APIView):

    def get(self, request):
        pidx = request.GET.get("pidx")

        if not pidx:
            return Response({"detail": "Missing pidx"}, status=400)

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"
        }

        response = requests.post(
            settings.KHALTI_VERIFY_URL,
            json={"pidx": pidx},
            headers=headers
        )

        data = response.json()
        print("Khalti response:", data)

        if data.get("status") != "Completed":
            return Response({"detail": "Payment not completed"}, status=400)

        # ✅ FIXED HERE
        try:
            payment = Payment.objects.get(txn_id=pidx)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found"}, status=404)

        bill = payment.bill

        with db_transaction.atomic():

            if bill.payment_status == PaymentStatus.SUCCESS:
                return Response({"detail": "Already paid"}, status=400)

            # update payment
            payment.status = PaymentStatus.SUCCESS
            payment.is_paid = True
            payment.save()

            # update bill
            bill.payment_status = PaymentStatus.SUCCESS
            bill.status = BillStatus.PAID
            bill.save()

        return Response({"message": "Payment successful"})

# -------------------------
# LIST USER TRANSACTIONS
# -------------------------
class TransactionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            bill__user=self.request.user
        ).order_by("-created_at")


# -------------------------
# TRANSACTION DETAIL
# -------------------------
class TransactionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            bill__user=self.request.user
        )