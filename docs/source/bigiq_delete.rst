delete
======

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.delete

Example
-------

.. code-block:: python

    path = (
        "/mgmt/cm/adc-core/working-config/ltm/node"
        "?$filter=name eq '172.17.0.1'"
    )
    node_id = device.id(path)
    device.delete(f"/mgmt/cm/adc-core/working-config/ltm/node/{node_id}")

Explanation
-----------

You need to provide the ID of the object, and it will be deleted from the device.