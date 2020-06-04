task_wait
==========

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.task_wait

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
    device.task_wait(task)
    
Explanation
-----------

After the task has started, we can wait for its completion with the task_wait method.