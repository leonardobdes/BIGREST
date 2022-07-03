task_wait
==========

Code
----

.. automethod:: bigrest.bigip.BIGIP.task_wait

Example
-------

.. code-block:: python

    data = {}
    data["command"] = "save"
    task = device.task_start("/mgmt/tm/task/sys/config", data)
    device.task_wait(task)

Explanation
-----------

| After the task has started, we can wait for its completion with the task_wait method.