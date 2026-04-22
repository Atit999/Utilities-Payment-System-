from rest_framework.generics import ListAPIView
from providers.models import Provider, Service
from .serializers import ProviderSerializer, ServiceSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


class ProviderListView(ListAPIView):
    queryset = Provider.objects.filter(is_active=True)
    serializer_class = ProviderSerializer


from rest_framework.generics import ListAPIView
from providers.models import Provider, Service
from .serializers import ProviderSerializer, ServiceSerializer


class ProviderListView(ListAPIView):
    queryset = Provider.objects.filter(is_active=True)
    serializer_class = ProviderSerializer


class ServiceListView(ListAPIView):
    serializer_class = ServiceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="provider_id",
                description="Filter services by provider ID",
                required=False,
                type=int,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id')

        if provider_id:
            return Service.objects.filter(provider_id=provider_id, is_active=True)

        return Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer

    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id')
        return Service.objects.filter(provider_id=provider_id, is_active=True)
    serializer_class = ServiceSerializer

    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id')
        return Service.objects.filter(provider_id=provider_id, is_active=True)