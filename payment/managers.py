from django.db import models

from .enums import TransactionType


class TransferManager(models.Manager):
    def create(self, **kwargs):
        instance = super(TransferManager, self).create(**kwargs)
        amount, source, destination = kwargs.get('amount'), kwargs.get('source'), kwargs.get('destination')
        from .models import Transaction
        # create debit transaction from source and credit transaction to destination
        Transaction.objects.bulk_create([
            Transaction(amount=amount, transfer=instance, transaction_type=TransactionType.DEBIT, account=source),
            Transaction(amount=amount, transfer=instance, transaction_type=TransactionType.CREDIT, account=destination),
        ])
        return instance

