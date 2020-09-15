# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.

import json
import requests
import urllib3

# Internal Imports
# Import only with "from x import y", to simplify the code.

from ..common.exceptions import InvalidOptionError
from ..common.exceptions import RESTAPIError

# Disable urllib3 SSL warnings
urllib3.disable_warnings()


def rest_format(text: str) -> str:
    """
    Converts a string to be compatible with iControl REST API.

    Arguments:
        text: String to be converted.

    """

    text = text.replace("/", "~")
    text = text.replace("%", "%25")
    return text


def token(device: str, username: str, password: str,
          login_provider: str = "tmos",
          debug: str = None) -> str:
    """
    Gets a token from the device.

    Arguments:
        device: Name or IP of the device to send the REST requests.
        username: Username used to login to the device.
        password: Password used to login to the device.
        login_provider: Login provider used to authenticate the user.
        debug: Debug file name to be used to output the debug information.

    Exceptions:
        InvalidOptionError: Raised when invalid options are used as arguments.
    """

    # Required for 12.0.0, but not in 15.1.0
    auth = (username, password)
    data = {}
    data["username"] = username
    data["password"] = password
    data["loginProviderName"] = login_provider
    response = requests.post(
        f"https://{device}/mgmt/shared/authn/login",
        json=data, verify=False, auth=auth)
    if response.status_code != 200:
        raise RESTAPIError(response, debug)
    return response.json()["token"]["token"]


def refresh_token(device: str, username: str, password: str,
                  login_provider: str = "tmos",
                  debug: str = None) -> str:
    """
    Gets a refresh token from the device.

    Arguments:
        device: Name or IP of the device to send the REST requests.
        username: Username used to login to the device.
        password: Password used to login to the device.
        login_provider: Login provider used to authenticate the user.
        debug: Debug file name to be used to output the debug information.

    Exceptions:
        InvalidOptionError: Raised when invalid options are used as arguments.
    """

    # Required for 12.0.0, but not in 15.1.0
    auth = (username, password)
    data = {}
    data["username"] = username
    data["password"] = password
    data["loginProviderName"] = login_provider
    response = requests.post(
        f"https://{device}/mgmt/shared/authn/login",
        json=data, verify=False, auth=auth)
    if response.status_code != 200:
        raise RESTAPIError(response, debug)
    response_json = response.json()
    if "refreshToken" in response_json:
        return response.json()["refreshToken"]["token"]
    else:
        raise InvalidOptionError(
            "Refresh token only available in a BIG-IQ device.")


def debug_request(response):
    req = f"curl -k -X {response.request.method} {response.request.url}"
    for k, v in iter(response.request.headers.items()):
        req += f" -H {k}: {v}"
    if any(v == 'application/json' for k, v in iter(response.request.headers.items())):
        if response.request.body:
            kwargs = json.loads(response.request.body.decode('utf-8'))
            req += " -d '" + json.dumps(kwargs, sort_keys=True) + "'"
    return req
