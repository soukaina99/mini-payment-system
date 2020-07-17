import pytest
from django.conf import settings
from django.test import RequestFactory
from faker import Faker
from django.test import Client
from .payment.factories import UserFactory


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user)
    client.user = user
    return client


@pytest.fixture
def faker():
    return Faker()
