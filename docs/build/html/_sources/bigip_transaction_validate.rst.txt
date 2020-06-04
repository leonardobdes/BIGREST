transaction_validate
====================

Code
----

.. automethod:: bigrest.bigip.BIGIP.transaction_validate

Example
-------

.. code-block:: python

    try:
        device.transaction_validate()
    except RESTAPIError:
        print("Transaction failed.")
    else:
        device.transaction_commit()
        print("Transaction completed.")

Explanation
-----------

| Before committing the transaction we can also validate the transaction.
| This will evaluate if the transaction is likely to fail or not.

