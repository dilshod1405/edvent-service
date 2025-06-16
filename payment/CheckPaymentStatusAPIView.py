from payme.views import PaymeWebHookAPIView
from django.http import JsonResponse
from .models import Transaction

class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def get_transaction(self, transaction_id):
        try:
            return Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return None

    def handle_check_perform_transaction(self, params, *args, **kwargs):
        transaction_id = params['account']['id']
        amount = params['amount']  # tiyinlarda
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        if transaction.total_amount != amount:
            return self.error(-31001, 'Incorrect amount')

        return self.result({ "allow": True })

    def handle_create_transaction(self, params, *args, **kwargs):
        transaction_id = params['account']['id']
        payme_transaction_id = params['id']
        amount = params['amount']

        transaction = self.get_transaction(transaction_id)
        if not transaction:
            return self.error(-31050, 'Transaction not found')

        if transaction.total_amount != amount:
            return self.error(-31001, 'Incorrect amount')

        if transaction.state != 'waiting':
            return self.error(-31008, 'Transaction already created or in wrong state')

        transaction.payme_transaction_id = payme_transaction_id
        transaction.state = 'waiting'
        transaction.save()

        return self.result({
            "create_time": str(transaction.created_at.timestamp() * 1000),
            "transaction": transaction.id,
            "state": 1  # waiting
        })

    def handle_perform_transaction(self, params, *args, **kwargs):
        transaction_id = params['account']['id']
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        if transaction.state == 'paid':
            return self.result({
                "transaction": transaction.id,
                "perform_time": str(transaction.updated_at.timestamp() * 1000),
                "state": 2
            })

        transaction.state = 'paid'
        transaction.save()

        return self.result({
            "transaction": transaction.id,
            "perform_time": str(transaction.updated_at.timestamp() * 1000),
            "state": 2
        })

    def handle_cancel_transaction(self, params, *args, **kwargs):
        transaction_id = params['account']['id']
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        transaction.state = 'canceled'
        transaction.save()

        return self.result({
            "transaction": transaction.id,
            "cancel_time": str(transaction.updated_at.timestamp() * 1000),
            "state": -1
        })

    def handle_check_transaction(self, params, *args, **kwargs):
        transaction_id = params['account']['id']
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        return self.result({
            "create_time": str(transaction.created_at.timestamp() * 1000),
            "perform_time": str(transaction.updated_at.timestamp() * 1000),
            "cancel_time": None if transaction.state != 'canceled' else str(transaction.updated_at.timestamp() * 1000),
            "transaction": transaction.id,
            "state": self.map_state(transaction.state)
        })

    def map_state(self, state):
        return {
            'waiting': 1,
            'paid': 2,
            'canceled': -1,
            'failed': -2
        }.get(state, 0)
