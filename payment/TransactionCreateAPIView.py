from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .models import Transaction
from .serializers import TransactionSerializer
from payme import Payme  # Siz ishlatayotgan SDK

class TransactionCreateAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Create the transaction object first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(user=request.user)

        # Generate Payme pay link
        payme = Payme(settings.PAYME_ID)
        pay_link = payme.initializer.generate_pay_link(
            id=transaction.id,
            amount=transaction.amount * 100,  # Payme expects tiyin
            return_url="https://edvent.uz"
        )

        # Return both transaction data and payment link
        return Response({
            "transaction": TransactionSerializer(transaction).data,
            "payme_link": pay_link
        }, status=status.HTTP_201_CREATED)
