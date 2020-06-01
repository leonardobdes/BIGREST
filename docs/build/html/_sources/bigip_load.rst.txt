load
=====

Code
----

.. automethod:: bigrest.bigip.BIGIP.load

Example
-------

.. code-block:: python

    virtuals = device.load("/mgmt/tm/ltm/virtual")
    virtual = device.load("/mgmt/tm/ltm/virtual/bigrest_vs")[0]

Explanation
-----------

| This will load objects from the device.
| This will always return a list of RESTObjects.

| The fist line will load all virtual servers from the device.
| You can then use a "for" to loop thought the virtual servers one by one.

| Last line loads a single virtual server.
| As the name of the virtual server was provided, we know it will only return a single object, so we use [0] to get the object (first object of the list).