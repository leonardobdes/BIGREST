link
=====

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.link

Example
-------

.. code-block:: python

    path = (
        "/mgmt/shared/resolver/device-groups/cm-adccore-allbigipDevices/devices"
        "?$filter=hostname eq 'LABBIGIP1.lab.local'"
    )
    device_link = device.link(path)

Explanation
-----------

| BIG-IQ API requires a link every time you want to reference another object.
| For example, if you want to associate a pool to a virtual server, you need to provide the link of the pool object.

| In this example, we want the link of the device.
| When we create a new object, we indicate that link as the device that the object should be linked.

| The method link helps with this task, as it will return the link for the type of object you want.

| The text to be queried has to use single quotes, in this example 'LABBIGIP1.lab.local'.