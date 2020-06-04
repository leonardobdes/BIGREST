save
=====

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.save

Example
-------

.. code-block:: python

    path = (
        "/mgmt/cm/adc-core/working-config/ltm/virtual"
        "?$filter=name eq 'bigrest_vs'"
    )
    virtual_id = device.id(path)
    virtual = device.load(
        f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id}")[0]
    path = (
        "/mgmt/cm/adc-core/working-config/ltm/pool"
        "?$filter=name eq 'bigrest_pool'"
    )
    pool_link = device.link(path)
    virtual.properties["poolReference"] = {"link": f"{pool_link}"}
    device.save(virtual)

Explanation
-----------

| After you load the object from the device, you can edit its properties.
| However, the modifications you do are local, so you need to send the modified object to the device.
| You do this using the method save, and passing the object to be saved.