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

    def validate(self, data):
        selected = [data.get('course'), data.get('module'), data.get('tariff')]
        if sum(1 for i in selected if i is not None) != 1:
            raise serializers.ValidationError("Faqat bitta (course YOKI module YOKI tariff) tanlanishi kerak.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
