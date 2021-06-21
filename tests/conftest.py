import pytest

from bigrest.bigip import BIGIP


def pytest_addoption(parser):
    parser.addoption("--bigip", action="store",
                     help="BIG-IP hostname or IP address", default="ltm3.test.local")
    parser.addoption("--username", action="store", help="BIG-IP REST username",
                     default="admin")
    parser.addoption("--password", action="store", help="BIG-IP REST password",
                     default="admin")


@pytest.fixture(scope='session')
def opt_bigip(request):
    return request.config.getoption("--bigip")


@pytest.fixture(scope='session')
def opt_username(request):
    return request.config.getoption("--username")


@pytest.fixture(scope='session')
def opt_password(request):
    return request.config.getoption("--password")


@pytest.fixture(scope='session')
def bigrest_root(opt_bigip, opt_username, opt_password):
    '''bigip fixture'''
    b = BIGIP(opt_bigip, opt_username, opt_password)
    return b
