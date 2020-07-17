from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, SubFactory, Sequence

from payment.models import Account, Transfer, Transaction


class UserFactory(DjangoModelFactory):
    username = Sequence(lambda n: 'user_name-%s' % n)

    class Meta:
        model = get_user_model()
        # django_get_or_create = ['username']


class AccountFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = Account


class TransferFactory(DjangoModelFactory):
    class Meta:
        model = Transfer


class TransactionFactory(DjangoModelFactory):
    account = SubFactory(AccountFactory)
    amount = 10.000
    class Meta:
        model = Transaction
