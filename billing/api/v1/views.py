from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from billing.models import Bill
from .serializers import BillSerializer


# -------------------------
# LIST + CREATE BILLS
# -------------------------
class BillListCreateView(ListCreateAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    # Optional: filtering + search
    filter_backends = [filters.SearchFilter]
    search_fields = ["account_number", "service__name"]

    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user).select_related("service")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -------------------------
# BILL DETAIL
# -------------------------
class BillDetailView(RetrieveAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user).select_related("service")