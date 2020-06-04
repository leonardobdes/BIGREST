RESTObject
==========

Code
----

.. autoclass:: bigrest.common.restobject.RESTObject

Example
-------

.. code-block:: python

    virtuals = device.load("/mgmt/tm/ltm/virtual")
    for virtual in virtuals:
        print(virtual.properties["name"])
        print(virtual)

Explanation
-----------

| BIGREST creates a RESTObject object with the response of an HTTP request sent to the iControl REST API.
| You can query the properties of the object using the properties attribute that is a Python dictionary.

| In the example above, the first print will print just the name of the virtual server.
| The next print will print the RESTObject.
| The RESTObject has a method to deal with the print function, so it will print the properties in a JSON format.