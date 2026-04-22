

from rest_framework import serializers
from billing.models import Bill


class BillSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source='service.provider.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ['user', 'status', 'payment_status']