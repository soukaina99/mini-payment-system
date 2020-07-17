from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path('payment/', include('payment.urls')),
    path('', lambda request: HttpResponse('alive!'), name='ping'),

]
