from payme.views import PaymeWebHookAPIView
from .models import Transaction

class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account']['id']
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.payme_transaction_id = result['transaction']
        transaction.state = 1  # Optional: depends on your business logic
        transaction.save()
        print("Payment created:", transaction.id)

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account']['id']
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.state = 1  # Paid
        transaction.save()
        print("Payment success:", transaction.id)

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account']['id']
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.state = -1  # Cancelled
        transaction.save()
        print("Payment cancelled:", transaction.id)

    def handle_failed_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account']['id']
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.state = -2  # Failed
        transaction.save()
        print("Payment failed:", transaction.id)