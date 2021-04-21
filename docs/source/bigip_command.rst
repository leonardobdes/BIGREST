command
=======

Code
----

.. automethod:: bigrest.bigip.BIGIP.command

Example
-------

.. code-block:: python

    data = {}
    data["command"] = "run"
    data["utilCmdArgs"] = "-c 'cat /VERSION'"
    result = device.command("/mgmt/tm/util/bash", data)
    print(result)

Explanation
-----------

| This runs a command on the device, and provides the result of the command if any is provided.
| You create a dictionary with the options you want and pass that to the command method.

| In this example, we are running the cat command via Bash.
| The result is saved to the variable "result", and we print that variable.