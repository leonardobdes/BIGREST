BIGIP
=====

Code
----

.. autoclass:: bigrest.bigip.BIGIP

Example
-------

.. code-block:: python

    device = BIGIP("192.168.255.1", "admin", "password")

Explanation
-----------

| Use this class to create a object that represents a BIG-IP device.
| When the object is create, BIGREST will try to connect to the device and report an error if can't.

| If you pass the debug keyword with filename, when iControl REST API returns an error, BIGREST will create the file with debug information.
| The information will include the full request sent to the device, and the full response received from the device.