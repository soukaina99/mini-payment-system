from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from payment.rest.views import TransferViewSet, AccountViewSet, TransactionViewSet

router = DefaultRouter()

router.register(r'transfer', TransferViewSet)
router.register(r'balance', AccountViewSet)
router.register(r'transaction', TransactionViewSet, basename='transaction')


app_name = 'payment'
urlpatterns = [
    path('', include(router.urls)),
]
