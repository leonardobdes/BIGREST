exist
=====

Code
----

.. automethod:: bigrest.bigip.BIGIP.exist

Example
-------

.. code-block:: python

    if device.exist(f"/mgmt/tm/ltm/virtual/{rest_format("/bigrest/bigrest_vs")}"):
        print(f"Virtual server exists.")
    else:
        print(f"Virtual server does not exist.")

Explanation
-----------

| Verifies if the object exists.
| In this example, verifies if virtual server "/bigrest/bigrest_vs" exists on the device.