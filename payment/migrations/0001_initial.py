# Generated by Django 3.0.8 on 2020-07-16 20:46

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import payment.enums
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('CLOSED', 'CLOSED'), ('PAUSED', 'PAUSED')], default='ACTIVE', max_length=10)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_transfers', to='payment.Account')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_transfers', to='payment.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('INIT', 'INIT'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], default='INIT', max_length=100)),
                ('transaction_type', models.CharField(choices=[(payment.enums.TransactionType['DEBIT'], 'DEBIT'), (payment.enums.TransactionType['CREDIT'], 'CREDIT')], max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='payment.Account')),
                ('transfer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='payment.Transfer')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-created_at'],
            },
        ),
    ]