modify
======

Code
----

.. automethod:: bigrest.bigip.BIGIP.modify

Example
-------

.. code-block:: python

    data = {}
    data["description"] = "bigrest"
    pool_updated = device.modify(
        f"/mgmt/tm/ltm/pool/{rest_format("bigrest/bigrest_pool")}", data)

Explanation
-----------

| If you just want to modify the properties of the object, instead of load and save, you can modify the object.
| You create a dictionary with the properties to be modified and pass that to the modify method.