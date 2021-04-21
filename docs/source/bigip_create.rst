create
======

Code
----

.. automethod:: bigrest.bigip.BIGIP.create

Example
-------

.. code-block:: python

    data = {}
    data["name"] = "bigrest"
    data["partition"] = "/"
    device.create("/mgmt/tm/sys/folder", data)

Explanation
-----------

| This will create a partition called bigrest.
| You create a dictionary with the properties of the new object and pass that to the create method.
| The system will use the default settings for any properties not specified.