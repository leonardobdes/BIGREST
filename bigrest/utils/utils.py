# External Imports
# Import only with 'import package',
# it will make explicity in the code where it came from.

import requests
import urllib3

# Internal Imports
# Import only with 'from x import y', to simplify the code.

from bigrest.common.exceptions import InvalidOptionError
from bigrest.common.exceptions import RESTAPIError

# Disable urllib3 SSL warnings
urllib3.disable_warnings()


def rest_format(text: str) -> str:
    """Convert a string to be compatible with iControl REST API."""

    text = text.replace('/', '~')
    text = text.replace('%', '%25')
    return text


def get_token(device: str, username: str, password: str,
              *, login_provider: str = 'local') -> str:
    """Get a token from the device."""

    data = {}
    data['username'] = username
    data['password'] = password
    data['loginProviderName'] = login_provider
    response = requests.post(
        f'https://{device}/mgmt/shared/authn/login', json=data, verify=False)
    if response.status_code != 200:
        raise RESTAPIError(response)
    return response.json()['token']['token']


def get_refresh_token(device: str, username: str, password: str,
                      *, login_provider: str = 'local') -> str:
    """Get a refresh token from the device."""

    data = {}
    data['username'] = username
    data['password'] = password
    data['loginProviderName'] = login_provider
    response = requests.post(
        f'https://{device}/mgmt/shared/authn/login', json=data, verify=False)
    if response.status_code != 200:
        raise RESTAPIError(response)
    response_json = response.json()
    if 'refreshToken' in response_json:
        return response.json()['refreshToken']['token']
    else:
        raise InvalidOptionError(
            'Refresh token only available in BIG-IQ devices.')
