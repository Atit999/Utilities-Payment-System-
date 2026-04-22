

from rest_framework import serializers
from payments.models import Payment, PaymentMethod


class PayBillSerializer(serializers.Serializer):
    model = Payment
    bill_id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=PaymentMethod.choices)