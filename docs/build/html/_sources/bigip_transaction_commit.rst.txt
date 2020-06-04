transaction_commit
==================

Code
----

.. automethod:: bigrest.bigip.BIGIP.transaction_commit

Example
-------

.. code-block:: python

    transaction_create = device.transaction_create()
    data = {}
    data["name"] = "/bigrest/bigrest_pool"
    device.create("/mgmt/tm/ltm/pool", data)
    data = {}
    data["name"] = "/bigrest/bigrest_vs"
    data["destination"] = "10.17.0.2%0:80"
    device.create("/mgmt/tm/ltm/virtual", data)
    device.transaction_commit()

Explanation
-----------

| Commit will run all commands you added to the transaction.
| In this context, commands are all actions you added to the transaction.

| In this example, we create a pool and a virtual server.
| However, they will only be created when we commit the transaction.
| Also, if one of the commands fails, all commands are canceled.