from django.urls import path
from .PaymeWebHookAPIView import PaymeCallBackAPIView
from .TransactionCreateAPIView import TransactionCreateAPIView
from .CheckPaymentStatusAPIView import CheckPaymentStatusAPIView
from .LessonListView import LessonListView

urlpatterns = [
    path("payme-callback/", PaymeCallBackAPIView.as_view(), name="payme-callback"),
    path("transactions/create/", TransactionCreateAPIView.as_view(), name="transaction-create"),
    path('check-payment-status/', CheckPaymentStatusAPIView.as_view(), name='check-payment-status'),
    path('lessons/', LessonListView.as_view(), name='lesson-list')
]
