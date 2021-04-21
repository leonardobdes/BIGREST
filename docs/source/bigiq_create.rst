create
======

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.create

Example
-------

.. code-block:: python

    path = (
        "/mgmt/shared/resolver/device-groups/cm-adccore-allbigipDevices/devices"
        "?$filter=hostname eq 'LABBIGIP1.lab.local'"
    )
    device_link = device.link(path)
    data = {
        "partition": "Common",
        "name": "172.17.0.1",
        "address": "172.17.0.1",
        "deviceReference": {
            "link": device_link
        }
    }
    device.create("/mgmt/cm/adc-core/working-config/ltm/node", data)

Explanation
-----------

| This will create a node on the device.
| You create a dictionary with the properties of the new object and pass that to the create method.
| The system will use the default settings for any properties not specified.