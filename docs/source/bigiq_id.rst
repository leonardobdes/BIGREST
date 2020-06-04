id
==

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.id

Example
-------

.. code-block:: python

    path = (
        "/mgmt/cm/adc-core/working-config/ltm/node"
        "?$filter=name eq '172.17.0.1'"
    )
    node_id = device.id(path)
    device.delete(f"/mgmt/cm/adc-core/working-config/ltm/node/{node_id}")

Explanation
-----------

| BIG-IQ API requires an ID every time you want to specify a single object.
| For example, if you want to delete an object, you need the object ID.

| In this example, we want the ID of the node.
| Then we delete the node using the ID we got.

| The method id helps with this task, as it will return the ID of the object you want.

| The text to be queried has to use single quotes, in this example '172.17.0.1'.