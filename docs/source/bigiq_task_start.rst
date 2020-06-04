task_start
==========

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.task_start

Example
-------

.. code-block:: python

    path = (
        f"/mgmt/shared/resolver/device-groups/cm-adccore-allbigipDevices/devices"
        f"?$filter=hostname eq 'LABBIGIP1.lab.local'"
    )
    device_link = device.link(path)
    path = (
        f"/mgmt/shared/resolver/device-groups/cm-adccore-allbigipDevices/devices"
        f"?$filter=hostname eq 'LABBIGIP2.lab.local'"
    )
    device_link2 = device.link(path)
    data = {
        "name": "BIGREST Add config to device",
        "deviceReferences": [
                {
                    "link": device_link
                },
                {
                    "link": device_link2
                }
        ],
        "disableUnusedObjectRemoval": True
    }
    device.task_start(
        "/mgmt/cm/adc-core/tasks/deploy-configuration", data)

Explanation
-----------

| Some HTTP requests sent to the iControl REST API will take some time to be completed.
| In these cases, they are defined as tasks.

| First, we create the properties of the task, and then we start the task.
| In this example, we are pushing the BIG-IQ configuration to the BIG-IP devices.