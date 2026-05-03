from django.urls import path
from .views import (
    InitiateKhaltiPaymentView,
    KhaltiCallbackView,
    TransactionListView,
    TransactionDetailView,
)

urlpatterns = [
    path("khalti/initiate/", InitiateKhaltiPaymentView.as_view(), name="initiate-payment"),
    path("khalti/callback/", KhaltiCallbackView.as_view(), name="khalti-callback"),

    path("transactions/", TransactionListView.as_view(), name="transactions"),
    path("transactions/<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
]