from rest_framework import serializers
from providers.models import Provider, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'code']


class ProviderSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        fields = ['id', 'name', 'code', 'services']