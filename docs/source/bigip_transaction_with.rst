Transaction with "with"
=======================

Example
-------

.. code-block:: python

    with device as transaction:
        data = {}
        data["name"] = "/bigrest/bigrest_pool"
        device.create("/mgmt/tm/ltm/pool", data)
        data = {}
        data["name"] = "/bigrest/bigrest_vs"
        data["destination"] = "10.17.0.3%0:80"
        device.create("/mgmt/tm/ltm/virtual", data)

Explanation
-----------

| To simplify the code you can use the "with" statement to create and commit a transaction.

| When the "with" starts, it will call the method transaction_create to create a transaction.
| When the "with" finishes, it will call the method transaction_commit to commit a transaction.

| You need to pass a BIGIP object to the "with", in this example we passed the "device" object.
| The transaction variable is not mandatory, so we could have just used "with device:".
| The transaction variable, or any other name you want to use, will be assigned the response from the transaction_create method.
| You can use that variable to get the transaction ID for example.
