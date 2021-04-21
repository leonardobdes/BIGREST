show
====

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.show

Example
-------

.. code-block:: python

    path = (
        "/mgmt/cm/adc-core/working-config/ltm/virtual"
        "?$filter=name eq 'bigrest_vs'"
    )
    virtual_id = device.id(path)
    virtual = device.show(
        f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id}")
    virtual_availability = virtual.properties[
        "status.availabilityState"]["description"]
    print(f"Virtual server status: {virtual_availability}")

Explanation
-----------

| This is simlar to tmsh show command.
| If the object properties includes another dictionary, keep adding keys until you find the value you need.
| In this example "status.availabilityState" property has a dictionary, and we want the value of the key "description".

| Similar to the method load, If called with an object name, it will just return a single object.
| If called without an object name, it will return a list with all object of that type.