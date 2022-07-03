BIGIQ
=====

Code
----

.. autoclass:: bigrest.bigiq.BIGIQ

Example
-------

.. code-block:: python

    device = BIGIQ("192.168.255.1", "admin", "password")

Explanation
-----------

| Use this class to create an object that represents a BIG-IQ device.
| When the object is created, BIGREST will try to connect to the device and report an error if it can't.

| If you pass the debug keyword with filename, when iControl REST API returns an error, BIGREST will create the file with debug information.
| The information will include the full HTTP request sent to the device, and the full HTTP response received from the device.
| It will also include a curl command you can use to test the request.
| For HTTP request with a binary body, curl command will end with "--data-binary @filename", replace filename with the file you were uploading.
| Take into account there is a limit of 1MB per HTTP request in the REST API, for large files you need to send the file in chunks.
| BIGREST does that automatically, but you need to do manually when using curl.

| By default the BIGREST will validate the SSL certificate, you can set session_verify=False to disable that.

| Timeout parameter defaults to 5 seconds, so it will wait up to 5 seconds for the device to response.