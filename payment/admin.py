from django.contrib import admin
from .models import Transaction, Transfer, Account

# Register your models here.
admin.site.register(Transfer)
admin.site.register(Transaction)
admin.site.register(Account)


