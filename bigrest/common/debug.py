"""Defines functions to be use for debug."""

# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
import requests
import json


def debug_data(response: requests.Response) -> str:
    """
    Provides information about the HTTP request
    and HTTP response to be used for troubleshooting.

    Arguments:
        response: A object created from a response to a HTTP request.
    """

    request_content_type = response.request.headers.get("Content-Type")
    reponse_content_type = response.headers.get("Content-Type")
    try:
        response_body = json.dumps(response.json(), indent=4)
    except Exception:
        if reponse_content_type == "application/octet-stream":
            response_body = "<binary data>"
        else:
            response_body = response.text
    response_status = response.status_code
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
            if request_content_type == "application/octet-stream":
                request_body = "<binary data>"
            else:
                request_body = response.text
    else:
        request_body = ""
    response_headers = response.headers
    response_headers = json.dumps(dict(response_headers), indent=4)
    information = (f"Request Method:\n{request_method}"
                   f"\nRequest URL:\n{request_url}"
                   f"\nRequest Headers:\n{request_headers}"
                   f"\nRequest Body:\n{request_body}"
                   f"\nResponse Status:\n{response_status}"
                   f"\nResponse Headers:\n{response_headers}"
                   f"\nResponse Body:\n{response_body}\n")
    return information


def debug_curl(response: requests.Response) -> str:
    """
    Converts a HTTP to a curl format to be used for troubleshooting.

    Arguments:
        response: A object created from a response to a HTTP request.
    """

    request = "Curl Command:\n"
    request += f"curl -k -X {response.request.method} {response.request.url}"
    headers = response.request.headers
    for header in headers:
        request += f" -H '{header}: {headers[header]}'"
    body = response.request.body
    if body is not None:
        try:
            json.dumps(body)
            request += f" -d '{body}'"
        except Exception:
            request += " --data-binary @filename"
    return "{request}\n"
