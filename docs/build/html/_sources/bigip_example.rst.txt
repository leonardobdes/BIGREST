Example
========

Code
----

.. automethod:: bigrest.bigip.BIGIP.example

Example
-------

.. code-block:: python

    node = device.example(f"/mgmt/tm/ltm/node")
    print("Print node example:")
    print(node)

Explanation
-----------

| Get an example representation of the object from the device.
| It provides a list of properties and also an explanation for each property.
| Similar to create an object via the GUI and select the help tab.