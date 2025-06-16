from payme.views import PaymeWebHookAPIView
from .models import Transaction

class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def get_transaction(self, transaction_id):
        try:
            return Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return None

    # === CheckPerformTransaction ===
    def handle_check_perform_transaction(self, params, *args, **kwargs):
        transaction_id = params['account'].get('id')
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        if transaction.amount != params['amount'] // 100:
            return self.error(-31001, 'Incorrect amount')

        return self.result({
            'allow': True
        })

    # === CreateTransaction ===
    def handle_created_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account'].get('id')
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        transaction.payme_transaction_id = result['transaction']
        transaction.state = 'waiting'
        transaction.save()

        return self.result({
            "create_time": result['create_time'],
            "transaction": result['transaction'],
            "state": 1
        })

    # === PerformTransaction ===
    def handle_successfully_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account'].get('id')
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        transaction.state = 'paid'
        transaction.save()

        return self.result({
            "transaction": result['transaction'],
            "perform_time": result['perform_time'],
            "state": 2
        })

    # === CancelTransaction ===
    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        transaction_id = params['account'].get('id')
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        transaction.state = 'canceled'
        transaction.save()

        return self.result({
            "transaction": result['transaction'],
            "cancel_time": result['cancel_time'],
            "state": -1
        })

    # === CheckTransaction ===
    def handle_check_transaction(self, params, result, *args, **kwargs):
        transaction_id = params['account'].get('id')
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            return self.error(-31050, 'Transaction not found')

        return self.result({
            "create_time": result.get('create_time', 0),
            "perform_time": result.get('perform_time', 0),
            "cancel_time": result.get('cancel_time', 0),
            "transaction": result['transaction'],
            "state": self.get_state_code(transaction.state),
            "reason": None
        })

    # === GetStatement ===
    def handle_get_statement(self, params, *args, **kwargs):
        # For basic implementation, return empty list
        return self.result({
            "transactions": []
        })

    # Helper method to map state
    def get_state_code(self, state):
        return {
            'created': 0,
            'waiting': 1,
            'paid': 2,
            'canceled': -1,
            'failed': -2,
        }.get(state, 0)
