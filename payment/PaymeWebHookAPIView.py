from payme.views import PaymeWebHookAPIView
from .models import Transaction

class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account']['id']
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.payme_transaction_id = result['transaction']
            transaction.state = 'waiting'  # To‘lov boshlandi, hali yakunlanmagan
            transaction.save()
            print("Payment created:", transaction.id)
        except Transaction.DoesNotExist:
            print("Transaction not found")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account']['id']
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.state = 'paid'
            transaction.save()
            print("Payment success:", transaction.id)
        except Transaction.DoesNotExist:
            print("Transaction not found")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account']['id']
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.state = 'canceled'
            transaction.save()
            print("Payment cancelled:", transaction.id)
        except Transaction.DoesNotExist:
            print("Transaction not found")

    def handle_failed_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account']['id']
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.state = 'failed'
            transaction.save()
            print("Payment failed:", transaction.id)
        except Transaction.DoesNotExist:
            print("Transaction not found")
