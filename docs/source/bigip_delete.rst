delete
======

Code
----

.. automethod:: bigrest.bigip.BIGIP.delete

Example
-------

.. code-block:: python

    device.delete(f"/mgmt/tm/ltm/node/{rest_format("/bigrest/172.17.0.1")}")

Explanation
-----------

You provide the full path for the object, and it will be deleted from the device.