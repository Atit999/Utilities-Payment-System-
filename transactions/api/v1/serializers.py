from rest_framework import serializers


class InitiatePaymentSerializer(serializers.Serializer):
    bill_id = serializers.IntegerField()


class VerifyPaymentSerializer(serializers.Serializer):
    pidx = serializers.CharField()