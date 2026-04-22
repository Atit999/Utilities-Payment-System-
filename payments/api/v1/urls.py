

from django.urls import path
from .views import PayBillView

urlpatterns = [
    path('pay/', PayBillView.as_view()),
]