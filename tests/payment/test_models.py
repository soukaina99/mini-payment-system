import pytest
from tests.payment.factories import AccountFactory, TransferFactory
from payment.enums import AccountStatus


@pytest.mark.django_db
def test_source_different_than_destination():
    """ this will test if source account is diffrent than destination
    """
    source = AccountFactory.create(balance=8000)
    with pytest.raises(Exception) as error:
        TransferFactory.create(source=source, destination=source, amount=90)
    assert 'Source must be diffrent than destination' in str(error.value)


@pytest.mark.django_db
def test_source_transfer_permission():
    """ this will test if source account is permitted to transfer when amount > balance
    """
    source = AccountFactory.create(balance=80)
    destination = AccountFactory.create()
    with pytest.raises(Exception) as error:
        TransferFactory.create(source=source, destination=destination, amount=100)
    assert 'Operation is not permitted' in str(error.value)


@pytest.mark.django_db
def test_destination_is_active():
    """ this will test if  account is permitted to transfer when destination account is not active
    """
    source = AccountFactory.create(balance=800)
    destination = AccountFactory.create(status=AccountStatus.CLOSED.value)
    with pytest.raises(Exception) as error:
        TransferFactory.create(source=source, destination=destination, amount=100)
    assert 'Destination account must be active' in str(error.value)
