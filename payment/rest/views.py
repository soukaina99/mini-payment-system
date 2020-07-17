from rest_framework import viewsets, mixins
import datetime
from payment.models import Transfer, Account, Transaction
from payment.rest.serializers import TransferSerializer, AccountSerializer, TransactionSerializer


class TransferViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin):
    """
    Transfer an amount to an account
    """
    # permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TransferSerializer
    queryset = Transfer.objects.all()


class AccountViewSet(viewsets.GenericViewSet,
                     mixins.RetrieveModelMixin):
    """
      get user account balance
    """
    # permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class TransactionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin):
    """
      get list of transactions
    """
    # permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.all()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(post_date__range=[start_date, end_date])
        return queryset
