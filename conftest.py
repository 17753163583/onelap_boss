import pytest


@pytest.fixture()
def boss_account_dict(request):
    account_dict = request.account_dict
    return account_dict
