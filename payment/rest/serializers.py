from django.conf import settings
from rest_framework import serializers
from django.utils import timezone
from payment.models import Transfer, Transaction, Account


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('source', 'destination', 'amount',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('uuid', 'account', 'status', 'transaction_type', 'amount',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('balance',)
