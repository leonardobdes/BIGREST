import pytest

from bigrest.bigip import BIGIP
from bigrest.common.exceptions import InvalidOptionError


def test_invalid_args():
    with pytest.raises(TypeError) as err:
        BIGIP('FakeHostName', 'admin', 'admin', badkwarg='devcentral')
    assert 'unexpected keyword' in str(err.value)


def test_multiple_token_options():
    with pytest.raises(InvalidOptionError) as err:
        BIGIP('ltm.test.local', 'admin', 'admin', request_token=True, token='THISISABADTOKEN')
    assert 'Use only one option' in str(err.value)
