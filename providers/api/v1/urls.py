from django.urls import path
from .views import ProviderListView, ServiceListView

urlpatterns = [
    path('providers/', ProviderListView.as_view()),
    path('services/', ServiceListView.as_view()),
]