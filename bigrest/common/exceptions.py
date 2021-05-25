"""Defines a list of exceptions."""

# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
import requests
import json

# Internal Imports
# Import only with "from x import y", to simplify the code.
from .debug import debug_data
from .debug import debug_curl


class Error(Exception):
    """Base class for all SDK exceptions."""
    pass


class RESTAPIError(Error):
    """
    Exception for API errors from iControl REST API.

    Arguments:
        response: A object created from a response to a HTTP request.
        debug: If set, indicates the file to save the debug output created.
    """

    def __init__(self, response: requests.Response,
                 debug: str) -> RESTAPIError:
        if debug is not None:
            with open(debug, "a") as file_:
                file_.write(debug_data(response))
                file_.write(debug_curl(response))
                super().__init__(f"Debug information saved in file {debug}.")
        else:
            reponse_content_type = response.headers.get("Content-Type")
            try:
                response_json = json.dumps(response.json(), indent=4)
                response_body = f"\nResponse Body:\n{response_json}"
            except Exception:
                if reponse_content_type == "application/octet-stream":
                    response_body = "\nResponse Body:\n<binary data>"
                else:
                    response_body = f"\nResponse Body:\n{response.text}"
            response_status = response.status_code
            information = f"\nStatus:\n{response_status}"
            super().__init__(f"{information}{response_body}")


class InvalidOptionError(Error):
    """
    Exception raised for invalid options passed.

    Arguments:
        message: Message that will be printed with the exception.
    """
    def __init__(self, message: str) -> InvalidOptionError:
        super().__init__(message)
