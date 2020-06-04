# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
import time

# Internal Imports
# Import only with "from x import y", to simplify the code.
from .big import BIG
from .common.exceptions import RESTAPIError
from .common.restobject import RESTObject


class BIGIQ(BIG):
    """
    Defines methods to call the iControl REST API that can be used by BIG-IQ.

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

    def task_start(self, path: str, data: dict) -> RESTObject:
        """
        Starts a task on the device.

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
        if response.status_code != 202:
            raise RESTAPIError(response, self.debug)
        return RESTObject(response.json())

    def task_wait(self, obj: RESTObject, interval: int = 10) -> None:
        """
        Continually queries the status of the task until it finishes.

        Sends an HTTP GET request to the iControl REST API.

        Arguments:
            obj: Object that represents the task.
            interval: The interval the queries will be made.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        path = self._get_path(obj)
        url = self._get_url(path)
        while True:
            if self.request_token or self.refresh_token is not None:
                self._check_token()
            response = self.session.get(url)
            if response.status_code != 200:
                raise RESTAPIError(response, self.debug)
            status = response.json()["status"]
            if status == "FAILED":
                raise RESTAPIError(response, self.debug)
            if status == "FINISHED":
                return
            else:
                time.sleep(interval)

    def task_completed(self, obj: RESTObject) -> bool:
        """
        Verifies if the task is completed.

        Sends an HTTP GET request to the iControl REST API.

        Arguments:
            obj: Object that represents the task.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        path = self._get_path(obj)
        url = self._get_url(path)
        response = self.session.get(url)
        if response.status_code != 200:
            raise RESTAPIError(response, self.debug)
        status = response.json()["status"]
        if status == "FAILED":
            raise RESTAPIError(response, self.debug)
        if status == "FINISHED":
            return True
        else:
            return False

    def exist(self, path: str) -> bool:
        """
        Verifies if the object exists on the device.

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
        if response_json["items"]:
            return True
        else:
            return False

    def link(self, path: str) -> str:
        """
        Get the link for the object.

        Sends an HTTP GET request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        obj = self.load(path)[0]
        return obj.properties["selfLink"]

    def id(self, path: str) -> str:
        """
        Get the ID of the object.

        Sends an HTTP GET request to the iControl REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.

        Exceptions:
            RESTAPIError: Raised when iControl REST API returns an error.
        """

        obj = self.load(path)[0]
        link = obj.properties["selfLink"]
        id_ = link.split("/")[-1]
        return id_
