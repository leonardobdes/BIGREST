load
=====

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.load

Example
-------

.. code-block:: python

    path = (
        "/mgmt/cm/adc-core/working-config/ltm/virtual"
        "?$filter=name eq 'bigrest_vs'"
    )
    virtual_id = device.id(path)
    virtual = device.load(f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id}")
    virtuals = device.load("/mgmt/cm/adc-core/working-config/ltm/virtual")

Explanation
-----------

| This will load one or multiple objects from the device.
| If called with an object name, it will just return a single object.
| If called without an object name, it will return a list with all object of that type.

| The first lines load a single virtual server.
| As the name of the virtual server was provided, we know it will only return a single object.

| The last line will load all virtual servers from the device.
| You can then use a "for" to loop thought the virtual servers one by one.
