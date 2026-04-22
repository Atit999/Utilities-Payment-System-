

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from billing.models import Bill, BillStatus, PaymentStatus as BillPaymentStatus
from payments.models import Payment, PaymentStatus
from .serializers import PayBillSerializer
import uuid


class PayBillView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PayBillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bill_id = serializer.validated_data['bill_id']
        method = serializer.validated_data['method']

        try:
            bill = Bill.objects.get(id=bill_id, user=request.user)
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=404)

        
        if bill.status == BillStatus.PAID:
            return Response({"error": "Bill already paid"}, status=400)

        if bill.payment_status == BillPaymentStatus.SUCCESS:
            return Response({"error": "Payment already completed"}, status=400)

        with transaction.atomic():

            # create payment
            payment = Payment.objects.create(
                user=request.user,
                bill=bill,
                method=method,
                amount=bill.amount,
                status=PaymentStatus.SUCCESS,  # simulate success
                txn_id=str(uuid.uuid4())
            )

            # update bill
            bill.status = BillStatus.PAID
            bill.payment_status = BillPaymentStatus.SUCCESS
            bill.save()

        return Response({
            "message": "Payment successful",
            "txn_id": payment.txn_id
        })