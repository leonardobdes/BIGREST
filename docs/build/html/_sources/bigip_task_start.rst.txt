task_start
==========

Code
----

.. automethod:: bigrest.bigip.BIGIP.task_start

Example
-------

.. code-block:: python

    data = {}
    data["command"] = "save"
    device.task_start("/mgmt/tm/task/sys/config", data)

Explanation
-----------

| Some HTTP requests sent to the iControl REST API will take some time to be completed.
| In these cases, they are defined as tasks.

| First, we create the properties of the task, and then we start the task.
| In this example, we are saving the configuration.