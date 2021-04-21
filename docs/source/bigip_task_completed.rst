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
    
     <more Python code here>

    if device.task_completed(task):
        print("Task test completed.")

Explanation
-----------

| Indicates if the task has finished, returning true or false.
| If you don't wait for the task to complete, you can run more Python code, and check the task later.