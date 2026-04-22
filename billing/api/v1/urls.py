
from django.urls import path
from .views import BillListCreateView, BillDetailView

urlpatterns = [
    path('bills/', BillListCreateView.as_view()),
    path('bills/<int:pk>/', BillDetailView.as_view()),
]