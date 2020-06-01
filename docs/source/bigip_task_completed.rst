task_completed
==============

Code
----

.. automethod:: bigrest.bigip.BIGIP.task_completed

Example
-------

.. code-block:: python

    data = {}
    data["command"] = "save"
    task = device.task_start("/mgmt/tm/task/sys/config", data)
    device.task_wait(task)
    if device.task_completed(task):
        print("Task test completed.")

Explanation
-----------

| Indicates if the tasks has finished, returning true or false.