Utils
=====

| BIGREST has a Python module called utils that has multiple useful functions.
| Use these functions to help you work with iControl REST API.

rest_format
-----------

Code
~~~~

.. autofunction:: bigrest.utils.utils.rest_format

Example
~~~~~~~

.. code-block:: python

    path = (
        f"/mgmt/tm/ltm/pool/{rest_format('/bigrest/bigrest_pool')}"
        f"/members/{rest_format('/bigrest/172.17.0.1%1:80')}"
    )
    device.delete(path)

Explanation
~~~~~~~~~~~

| iControl REST API requires "/" to be converted to "~".
| Also requires "%" (used for route domains) to be converted to "%25".

token
-----

Code
~~~~

.. autofunction:: bigrest.utils.utils.token

Example
~~~~~~~

.. code-block:: python

    token_ = token("192.168.255.1", "admin", "password")

Explanation
~~~~~~~~~~~

| This function is mainly used to test the BIGREST itself.
| However, you can use to generate a token, that can be used in other tools.
| If you are just working with BIGREST, either BIGIP or BIGIQ classes, it can use token internally if you enable token.

| If you pass the debug keyword with filename, when iControl REST API returns an error, BIGREST will create the file with debug information.
| The information will include the HTTP full request sent to the device, and the HTTP full response received from the device.

refresh_token
-------------

Code
~~~~

.. autofunction:: bigrest.utils.utils.refresh_token

Example
~~~~~~~

.. code-block:: python

    refresh_token_ = refresh_token("192.168.255.1", "admin", "password")

Explanation
~~~~~~~~~~~

| This function is mainly used to test the BIGREST itself and only works with BIG-IQ (BIG-IP does not implement refresh token).
| However, you can use to generate a refresh token, that can be used in other tools.
| If you are just working with BIGREST, BIGIQ class only, it can use refresh token internally if you provide a refresh token.

| If you pass the debug keyword with filename, when iControl REST API returns an error, BIGREST will create the file with debug information.
| The information will include the HTTP full request sent to the device, and the full HTTP response received from the device.
