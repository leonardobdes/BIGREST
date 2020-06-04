load
=====

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.load

Example
-------

.. code-block:: python

    virtuals = device.load("/mgmt/cm/adc-core/working-config/ltm/virtual")
    path = (
        "/mgmt/cm/adc-core/working-config/ltm/virtual"
        "?$filter=name eq 'bigrest_vs'"
    )
    virtual_id = device.id(path)
    virtual = device.load(f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id})[0]

Explanation
-----------

| This will load objects from the device.
| This will always return a list of RESTObjects.

| The first line will load all virtual servers from the device.
| You can then use a "for" to loop thought the virtual servers one by one.

| The last line loads a single virtual server.
| As the virtual server ID was provided, we know it will only return a single object, so we use [0] to get the object (first object of the list).