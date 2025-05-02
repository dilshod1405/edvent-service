from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .models import Transaction
from .serializers import TransactionSerializer
from payme import Payme

class TransactionCreateAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        transaction_id = response.data['id']
        transaction = Transaction.objects.get(id=transaction_id)
        payme = Payme(settings.PAYME_ID)
        pay_link = payme.initializer.generate_pay_link(
            id=transaction.id,
            amount=transaction.amount,
            return_url="https://edvent.uz"
        )
        return Response({
            "transaction": response.data,
            "payme_link": pay_link
        }, status=status.HTTP_201_CREATED)
