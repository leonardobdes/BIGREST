task_result
===========

Code
----

.. automethod:: bigrest.bigip.BIGIP.task_result

Example
-------

.. code-block:: python

    data = {}
    data["command"] = "save"
    task = device.task_start("/mgmt/tm/task/sys/config", data)
    device.task_wait(task)
    if device.task_completed(task):
        print(device.task_result(task))

Explanation
-----------

| If the task produces a result, the method task_result will return the result string.