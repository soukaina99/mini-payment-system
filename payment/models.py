import uuid
from django.db import models

from decimal import Decimal as D

from django.contrib.auth.models import User
from .enums import AccountStatus,  TransactionStatus, TransactionType
from .managers import TransferManager
from rest_framework.serializers import ValidationError


# Create your models here.

class Account(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=D('0.00'),
        null=True
    )
    status = models.CharField(
        max_length=20,
        default=AccountStatus.ACTIVE.value,
        choices=[(tag.name, tag.value) for tag in AccountStatus]
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True
    )

    # audit fields
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.user.email

    @property
    def is_active(self):
        return self.status == AccountStatus.ACTIVE.value

    def operation_is_permitted(self, amount):
        return self.is_active and self.balance >= amount


class Transfer(models.Model):
    source = models.ForeignKey(
        Account,
        related_name='source_transfers',
        on_delete = models.CASCADE,
    )
    destination = models.ForeignKey(
        Account,
        related_name='destination_transfers',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    # audit fields
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    objects = TransferManager()

    def __str__(self):
        return self.source.user.email

    def clean(self):
        if self.source == self.destination:
            raise ValidationError("Source must be diffrent than destination")
        if not self.source.operation_is_permitted(self.amount):
            raise ValidationError("Operation is not permitted")
        if not self.destination.is_active:
            raise ValidationError("Destination account must be active")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Transfer, self).save()



class Transaction(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    transfer = models.ForeignKey(
        Transfer,
        related_name="transactions",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    status = models.CharField(
        max_length=100,
        default=TransactionStatus.INIT.value,
        choices=[(item.name, item.value) for item in TransactionStatus]
    )
    transaction_type = models.CharField(
        max_length=100,
        choices=[(item, item.value) for item in TransactionType]
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    # audit fields
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    post_date = models.DateTimeField('Post date', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return self.account.user.email
