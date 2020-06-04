modify
======

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.modify

Example
-------

.. code-block:: python

    path = (
        "/mgmt/cm/adc-core/working-config/ltm/pool"
        "?$filter=name eq 'bigrest_pool'"
    )
    pool_id = device.id(path)
    data = {}
    description = "bigrest"
    data["description"] = description
    pool_updated = device.modify(
        f"/mgmt/cm/adc-core/working-config/ltm/pool/{pool_id}", data)

Explanation
-----------

| If you just want to modify the properties of the object, instead of load and save, you can modify the object.
| You create a dictionary with the properties to be modified and pass that to the modify method.