show
====

Code
----

.. automethod:: bigrest.bigip.BIGIP.show

Example
-------

.. code-block:: python

    virtual = device.show(
        f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}")
    print(f'Maximum number of connections client side: {virtual.properties["clientside.maxConns"]["value"]}')

Explanation
-----------

| This is similar to tmsh show command.
| If the object property includes another dictionary, keep adding keys until you find the value you need.
| In this example "clientside.maxConns" property has a dictionary, and we want the value of the key "value".

| Similar to the method load, If called with an object name, it will just return a single object.
| If called without an object name, it will return a list with all object of that type.