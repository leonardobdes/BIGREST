task_completed
==============

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.task_completed

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
    task = device.task_start(
        "/mgmt/cm/adc-core/tasks/deploy-configuration", data)

    <more Python code here>

    if device.task_completed(task):
        print("Task test completed.")

Explanation
-----------

| Indicates if the task has finished, returning true or false.
| If you don't want to wait for the task to complete, you can run more Python code, and check the task later.
