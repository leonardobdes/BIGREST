save
=====

Code
----

.. automethod:: bigrest.bigip.BIGIP.save

Example
-------

.. code-block:: python

    virtual = device.load(
        "/mgmt/tm/ltm/virtual/bigrest_vs")[0]
    virtual.properties["pool"] = "bigrest_pool"
    device.save(virtual)

Explanation
-----------

| After you load the object from the device, you can edit its properties.
| However, the modifications you do are local, so you need to send the modified object to the device.
| You do this using the method save, and passing the object to be saved.