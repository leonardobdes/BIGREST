exist
=====

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.exist

Example
-------

.. code-block:: python

    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/virtual"
        f"?$filter=name eq 'bigrest_vs'"
    )
    if device.exist(path):
        print(f"Virtual server exists.")
    else:
        print(f"Virtual server does not exist.")

Explanation
-----------

| Verifies if the object exists.
| In this example, verifies if virtual server "bigrest_vs" exists on the device.