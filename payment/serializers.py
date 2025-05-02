from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'course',
            'module',
            'tariff',
            'amount',
            'payment_type',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Associate the authenticated user to the transaction
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
