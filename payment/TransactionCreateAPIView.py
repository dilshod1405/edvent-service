from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from config.settings import base as settings
from .models import Transaction
from .serializers import TransactionSerializer
from payme import Payme

# TransactionCreateAPIView
class TransactionCreateAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(user=request.user)

        amount_in_tiyin = int(transaction.amount)

        payme = Payme(settings.PAYME_ID, settings.PAYME_KEY)
        pay_link = payme.initializer.generate_pay_link(
            id=transaction.id,
            amount=amount_in_tiyin,
            return_url="https://edvent.uz/api/dashboard/kurslarim"
        )

        return Response({
            "transaction": TransactionSerializer(transaction).data,
            "payme_link": pay_link
        }, status=status.HTTP_201_CREATED)


