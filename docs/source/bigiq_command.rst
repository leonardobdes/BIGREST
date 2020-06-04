command
=======

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.command

Example
-------

.. code-block:: python

    data = {}
    data["command"] = "run"
    data["utilCmdArgs"] = "-c1 localhost"
    result = device.command("/mgmt/tm/util/ping", data)
    print(result)

Explanation
-----------

| This runs a command on the device and provides the result of the command if any is provided.
| You create a dictionary with the options you want and pass that to the command method.

| In this example, we are running the ping command.
| The result is saved to the variable "result", and we print that variable.

| BIG-IQ API does not allow the use of Bash commands.
| You can use the commands tmsh exposes, like dig/ping/telnet/traceroute/etc...
| You can also use some Unix commands, like unix-ls/unix-mv/unix-rm.