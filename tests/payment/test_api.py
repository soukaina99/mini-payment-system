import datetime
from decimal import Decimal as D

import pytest
from django.urls import reverse
from rest_framework import status

from tests.payment.factories import AccountFactory, TransactionFactory


@pytest.mark.django_db
def test_transfer_success(client):
    source = AccountFactory.create(balance=900)
    destination = AccountFactory.create()
    data = {
        "amount": 50,
        "source": source.uuid,
        "destination": destination.uuid,
    }
    response = client.post(reverse('payment:transfer-list'),
                           headers={"Content-Type": "application/json"},
                           data=data)
    assert response.status_code == status.HTTP_201_CREATED
    transfer = source.source_transfers.first()
    assert transfer
    assert transfer.transactions.count() == 2


@pytest.mark.django_db
def test_transfer_source_permission(client):
    source = AccountFactory.create(status='CLOSED')
    destination = AccountFactory.create()
    headers = {"Content-Type": "application/json",
               },
    data = {
        "amount": 50,
        "source": source.uuid,
        "destination": destination.uuid,
    }
    response = client.post(reverse('payment:transfer-list'),
                           headers={"Content-Type": "application/json"},
                           data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Operation is not permitted" in response.json()


@pytest.mark.django_db
def test_transfer_same_source_and_destination(client):
    source = AccountFactory.create(status='ACTIVE')
    data = {
        "amount": 50,
        "source": source.uuid,
        "destination": source.uuid,
    }
    response = client.post(reverse('payment:transfer-list'),
                           headers={"Content-Type": "application/json"},
                           data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Source must be diffrent than destination" in response.json()


@pytest.mark.django_db
def test_transfer_nonexistent_uuid(client):
    source = AccountFactory.create(status='ACTIVE')
    data = {
        "amount": 50,
        "source": source.uuid,
        "destination": 22,
    }
    response = client.post(reverse('payment:transfer-list'),
                           headers={"Content-Type": "application/json"},
                           data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "'22' is not a valid UUID." in response.json()['destination']


@pytest.mark.django_db
def test_get_balance(client):
    balance = D(200.00)
    account = AccountFactory.create(balance=balance)
    response = client.get(
        reverse('payment:account-detail', args={account.uuid})
    )
    assert response.status_code == status.HTTP_200_OK
    assert D(response.json()['balance']) == balance


@pytest.mark.django_db
def test_get_balance_nonexistent_uuid(client):
    response = client.get(
        reverse('payment:account-detail', args={"12bb"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


# @pytest.mark.django_db
# def test_get_all_transactions(client):
#     TransactionFactory.create_batch(4)
#     response = client.get(reverse('payment:transaction-list'),
#                            headers={"Content-Type": "application/json"})
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) == 4


@pytest.mark.django_db
def test_filter_transactions(client):
    TransactionFactory.create(post_date=datetime.datetime.now())
    transaction_b = TransactionFactory.create(post_date=datetime.datetime(2020, 7, 1, 0, 0))
    start_date = datetime.datetime(2020, 6, 1, 0, 0)
    end_date = datetime.datetime(2020, 7, 2, 0, 0)
    response = client.get(reverse('payment:transaction-list'),{'start_date': start_date, 'end_date': end_date},
                           headers={"Content-Type": "application/json"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]['uuid'] == str(transaction_b.uuid)