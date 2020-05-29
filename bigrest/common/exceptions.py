"""Defines a list of exceptions."""

# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
import requests
import json


class Error(Exception):
    """Base class for all SDK exceptions."""
    pass


class RESTAPIError(Error):
    """
    Exception for API errors from iControl REST API.

    Parameters:
        response: A object created from a response to a HTTP request.
        debug: If set, indicates the file to save the debug output created.
    """

    def __init__(self, response: requests.Response,
                 debug: str) -> RESTAPIError:
        reponse_content_type = response.headers.get("Content-Type")
        try:
            response_json = json.dumps(response.json(), indent=4)
            response_body = f"\nResponse Body:\n{response_json}"
        except Exception:
            if reponse_content_type == "application/octet-stream":
                response_body = f"\nResponse Body:\n{response.content}"
            else:
                response_body = f"\nResponse Body:\n{response.text}"
        response_status = response.status_code
        if debug is not None:
            request_method = response.request.method
            request_url = response.request.url
            request_headers = response.request.headers
            request_headers = json.dumps(dict(request_headers), indent=4)
            request_body = response.request.body
            if request_body is not None:
                try:
                    request_body = json.dumps(
                        dict(eval(request_body)), indent=4)
                except Exception:
                    pass
            else:
                request_body = ""
            response_headers = response.headers
            response_headers = json.dumps(dict(response_headers), indent=4)
            information = (f"Request Method:\n{request_method}"
                           f"\nRequest URL:\n{request_url}"
                           f"\nRequest headers:\n{request_headers}"
                           f"\nRequest body:\n{request_body}"
                           f"\nResponse Status:\n{response_status}"
                           f"\nResponse headers:\n{response_headers}")
            with open(debug, "w") as file_:
                file_.write(f"{information}{response_body}")
                super().__init__(f"Debug information saved in file {debug}.")
        else:
            information = f"\nStatus:\n{response_status}"
            super().__init__(f"{information}{response_body}")


class InvalidOptionError(Error):
    """
    Exception raised for invalid options passed.

    Parameters:
        message: Message that will be printed with the exception.
    """
    def __init__(self, message: str) -> InvalidOptionError:
        super().__init__(message)
