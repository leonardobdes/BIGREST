load
=====

Code
----

.. automethod:: bigrest.bigip.BIGIP.load

Example
-------

.. code-block:: python

    virtual = device.load("/mgmt/tm/ltm/virtual/bigrest_vs")
    virtuals = device.load("/mgmt/tm/ltm/virtual")

Explanation
-----------

| This will load one or multiple objects from the device.
| If called with an object name, it will just return a single object.
| If called without an object name, it will return a list with all object of that type.

| The first line loads a single virtual server.
| As the name of the virtual server was provided, we know it will only return a single object.

| The last line will load all virtual servers from the device.
| You can then use a "for" to loop thought the virtual servers one by one.