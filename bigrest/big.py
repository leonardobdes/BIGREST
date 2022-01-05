# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
from typing import Union
import requests
import time
import urllib3
import pathlib
import urllib

# Internal Imports
# Import only with "from x import y", to simplify the code.

from .common.restobject import RESTObject
from .common.exceptions import RESTAPIError
from .common.exceptions import InvalidOptionError
from .common.constants import TOKEN_EXTRA_TIME
from .common.constants import REST_API_MAXIMUM_CHUNK_SIZE
from .version import __version__

# Disable urllib3 SSL warnings
urllib3.disable_warnings()


class BIG:
    """
    Defines methods to call the iControl REST API that can be used
    by BIG-IP or BIG-IQ.

    Arguments:
        device: Name or IP of the device to send the HTTP requests.
        username: Username used to login to the device.
        password: Password used to login to the device.
        login_provider: Login provider used to authenticate the user.
        request_token: Indicates if a token should be requested from the
            device and used for HTTP requests.
        token: Token to be used to send HTTP requests to the device.
        refresh_token: Refresh token to be used to request new token,
            the new token will be then used for HTTP requests.
        debug: Debug file name to be used to output the debug information.

    Exceptions:
        InvalidOptionError: Raised when invalid options are used as arguments.
    """

    def __init__(self, device: str, username: str = None,
                 password: str = None, login_provider: str = "tmos",
                 request_token: bool = False, token: str = None,
                 refresh_token: str = None, debug: str = None) -> BIG:

        # Input validations
        message = (
            "Use only one option,"
            "request_token or token or refresh_token.")
        if request_token and token is not None:
            raise InvalidOptionError(message)
        if request_token and refresh_token is not None:
            raise InvalidOptionError(message)
        if token is not None and refresh_token is not None:
            raise InvalidOptionError(message)

        # Variables
        self.device = device
        self.username = username
        self.password = password
        self.request_token = request_token
        self.login_provider = login_provider
        self._token = None
        self._token_timeout = None
        self._token_counter = None
        self.token = token
        self.refresh_token = refresh_token
        self._transaction = None
        self.debug = debug
        self.session = requests.Session()

        # Session settings
        if self.request_token is False:
            self.session.auth = (username, password)
        if self.token is not None:
            self.session.headers.update({"X-F5-Auth-Token": f"{self.token}"})
        self.session.headers.update({"Content-Type": "application/json"})
        self.session.verify = False
        self.session.headers.update({"User-Agent": f"BIGREST/{__version__}"})

        # Connect to device
        self._connect()

    def load(self, path: str) -> Union[list[RESTObject], RESTObject]:
        """
        Loads one object or a list of objects from the device.
        If you call with a specific object name, it returns a single object.
        If you call without an object name, it returns a list of objects.

        Sends an HTTP GET request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        url = self._get_url(path)
        response = self.session.get(url)
        if response.status_code != 200:
            raise RESTAPIError(response, self.debug)
        response_json = response.json()
        if "items" in response_json:
            objects = []
            for obj in response_json["items"]:
                objects.append(RESTObject(obj))
            return objects
        else:
            return RESTObject(response_json)

    def save(self, obj: RESTObject) -> RESTObject:
        """
        Saves on the device the changes that were made locally to the object.

        Sends an HTTP PUT request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        path = self._get_path(obj)
        url = self._get_url(path)
        response = self.session.put(url, json=obj.asdict())
        if response.status_code != 200:
            raise RESTAPIError(response, self.debug)
        return RESTObject(response.json())

    def delete(self, path: str) -> None:
        """
        Deletes the object on the device.

        Sends an HTTP DELETE request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        url = self._get_url(path)
        response = self.session.delete(url)
        if response.status_code != 200:
            raise RESTAPIError(response, self.debug)

    def create(self, path: str, data: dict) -> RESTObject:
        """
        Creates the object on the device.

        Sends an HTTP POST request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.
            data: Payload that will be sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        url = self._get_url(path)
        response = self.session.post(url, json=data)
        if (response.status_code != 200 and
                response.status_code != 201 and
                response.status_code != 202):
            raise RESTAPIError(response, self.debug)
        return RESTObject(response.json())

    def modify(self, path: str, data: dict) -> RESTObject:
        """
        Modifies the object on the device.

        Sends an HTTP PATCH request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.
            data: Payload that will be sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        url = self._get_url(path)
        response = self.session.patch(url, json=data)
        if response.status_code != 200:
            raise RESTAPIError(response, self.debug)
        return RESTObject(response.json())

    def show(self, path: str) -> Union[list[RESTObject], RESTObject]:
        """
        Gets statistical information about the objects from the device.
        If you call with a specific object name, it returns a single object.
        If you call without an object name, it returns a list of objects.

        Similar to tmsh show command.

        Sends an HTTP GET request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        url = self._get_url(path)
        url = f"{url}/stats"
        response = self.session.get(url)
        if response.status_code != 200:
            raise RESTAPIError(response, self.debug)
        response_json = response.json()
        objects = []
        if "entries" in response_json:
            entries = response_json["entries"]
            for obj_name in entries:
                if "nestedStats" in entries[obj_name]:
                    objects.append(
                        RESTObject(
                            entries[obj_name]["nestedStats"]["entries"]))
                else:
                    objects.append(RESTObject(entries))
        else:
            objects.append(RESTObject(response_json))
        # "collection" for BIG-IP
        # "com.f5.rest.common" for BIG-IQ
        if ("collection" in response_json["kind"] or
                "com.f5.rest.common" in response_json["entries"]):
            return objects
        else:
            return objects[0]

    def command(self, path: str, data: dict) -> str:
        """
        Executes a command on the device.

        Sends an HTTP POST request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.
            data: Payload that will be sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        obj = self.create(path, data)
        if "commandResult" in obj.properties:
            return obj.properties["commandResult"]
        else:
            return str()

    def download(self, path: str, filename: str) -> None:
        """
        Downloads a file from the device.

        Sends an HTTP GET request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.
            filename: Name of the file to be downloaded.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        # Content-Range: <range-start>-<range-end>/<size>
        if self.request_token or self.refresh_token is not None:
            self._check_token()
        filename_without_path = pathlib.PurePath(filename).name
        url = self._get_url(path)
        url = f"{url}/{filename_without_path}"
        self.session.headers.update(
            {"Content-Type": "application/octet-stream"})
        range_size = REST_API_MAXIMUM_CHUNK_SIZE - 1
        self.session.headers.update(
            {"Content-Range": f"0-{range_size}/0"})
        response = self.session.get(url)
        if response.status_code != 200 and response.status_code != 206:
            raise RESTAPIError(self.esponse, self.debug)
        content_range = response.headers.get("Content-Range")
        range_start = range_size + 1
        range_end = range_start + range_size
        size = int(content_range.split("/")[1])
        size = size - 1
        with open(filename, "wb") as file_:
            file_.write(response.content)
            while size >= range_start:
                if range_end > size:
                    range_end = size
                content_range = f"{range_start}-{range_end}/{size + 1}"
                self.session.headers.update(
                    {"Content-Range": content_range})
                response = self.session.get(url)
                file_.write(response.content)
                if response.status_code != 200:
                    raise RESTAPIError(response, self.debug)
                range_start = range_end + 1
                range_end = range_end + range_size + 1
        self.session.headers.pop("Content-Range")
        self.session.headers.update({"Content-Type": "application/json"})

    def upload(self, path: str, filename: str) -> None:
        """
        Uploads a file to the device.

        Sends an HTTP POST request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.
            filename: Name of the file to be uploaded.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        # Content-Range: <range-start>-<range-end>/<size>
        if self.request_token or self.refresh_token is not None:
            self._check_token()
        self.session.headers.update(
            {"Content-Type": "application/octet-stream"})
        filename_without_path = pathlib.PurePath(filename).name
        url = self._get_url(path)
        url = f"{url}/{filename_without_path}"
        range_start = 0
        range_size = REST_API_MAXIMUM_CHUNK_SIZE - 1
        range_end = range_size
        size = pathlib.Path(filename).stat().st_size - 1
        with open(filename, "rb") as file_:
            if size <= range_size:
                self.session.headers.update(
                    {"Content-Range": f"{range_start}-{size}/{size + 1}"})
                response = self.session.post(url, data=file_.read(size + 1))
                if response.status_code != 200:
                    raise RESTAPIError(response, self.debug)
            else:
                while size >= range_start:
                    if range_end > size:
                        range_end = size
                    content_range = f"{range_start}-{range_end}/{size + 1}"
                    self.session.headers.update(
                        {"Content-Range": content_range})
                    bytes_to_read = (range_end - range_start) + 1
                    response = self.session.post(
                        url, data=file_.read(bytes_to_read))
                    if response.status_code != 200:
                        raise RESTAPIError(response, self.debug)
                    range_start = range_end + 1
                    range_end = range_end + range_size + 1
        self.session.headers.pop("Content-Range")
        self.session.headers.update({"Content-Type": "application/json"})

    def example(self, path: str) -> RESTObject:
        """
        Gets an example of an object from the device.

        Sends an HTTP GET request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        url = self._get_url(path)
        url = f"{url}/example"
        response = self.session.get(url)
        if response.status_code != 200:
            raise RESTAPIError(response, self.debug)
        return RESTObject(response.json())

    def _get_url(self, path: str) -> str:
        """
        Creates the URL to be used to connect to the device.

        Arguments:
            path: HTTP path used to create the URL.
        """

        if path.endswith("/"):
            path = path[:-1]
        return f"https://{self.device}{path}"

    def _check_token(self) -> None:
        """
        Verifies if there is a token to be used.

        If there is a token, it verifies if it is still valid.
        """

        if self._token is None:
            self._get_token()
        else:
            time_passed = time.time() - self._token_counter
            # Only use token if still valid for TOKEN_EXTRA_TIME seconds
            time_passed = time_passed + TOKEN_EXTRA_TIME
            if time_passed > self._token_timeout:
                self._get_token()

    def _get_token(self) -> None:
        """
        Gets a token from the device.

        Sends an HTTP POST request to the iControl REST API.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if "X-F5-Auth-Token" in self.session.headers:
            self.session.headers.pop("X-F5-Auth-Token")
        # Required for 12.0.0, but not in 15.1.0
        self.session.auth = (self.username, self.password)
        response = None
        if self.refresh_token is None:
            data = {}
            data["username"] = self.username
            data["password"] = self.password
            data["loginProviderName"] = self.login_provider
            response = self.session.post(
                f"https://{self.device}/mgmt/shared/authn/login", json=data)
        else:
            data_token = {}
            data_token["token"] = self.refresh_token
            data = {}
            data["refreshToken"] = data_token
            response = self.session.post(
                f"https://{self.device}/mgmt/shared/authn/exchange", json=data)
        if response.status_code != 200:
            raise RESTAPIError(response, self.debug)
        self._token_counter = time.time()
        self._token = response.json()["token"]["token"]
        self.session.headers.update({"X-F5-Auth-Token": f"{self._token}"})
        self._token_timeout = response.json()["token"]["timeout"]
        self.session.auth = None

    def _get_path(self, obj: RESTObject) -> str:
        """
        Gets the HTTP path from the object.

        Arguments:
            obj: Object to get the path from.
        """
        self_link = obj.properties["selfLink"]
        path = urllib.parse.urlparse(self_link).path
        return path

    def _connect(self) -> None:
        """
        Test a connection to the device.

        If resquest_token or refresh_token is set, tries to get a token.

        If using a token or basic authentication, sends an HTTP GET request
            to the iControl REST API to test the connection.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._get_token()
        else:
            response = self.session.get(
                f"https://{self.device}/mgmt/shared/echo-query")
            if response.status_code != 200:
                raise RESTAPIError(response, self.debug)
