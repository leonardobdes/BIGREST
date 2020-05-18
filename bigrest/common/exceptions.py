"""Define a list of exceptions."""

# External Imports
# Import only with 'import package',
# it will make explicity in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
from requests import Response


class Error(Exception):
    """Base class for exceptions"""
    pass


class RESTAPIError(Error):
    """Exception raised for API errors from iControl REST API."""

    def __init__(self, response: Response) -> RESTAPIError:
        try:
            response_json = response.json()
            code = response_json['code']
            message = response_json['message']
            super().__init__(f'Code: "{code}" Message: "{message}"')
        except Exception:
            code = response.status_code
            super().__init__(f'Code: "{code}"')


class InvalidOptionError(Error):
    """Exception raised for invalid options passed."""

    def __init__(self, message: str) -> InvalidOptionError:
        super().__init__(message)
