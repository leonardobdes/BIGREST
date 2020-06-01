show
====

Code
----

.. automethod:: bigrest.bigip.BIGIP.show

Example
-------

.. code-block:: python

    virtual = device.show(
        f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}")[0]
    print(f'Maximum number of connections client side: {virtual.properties["clientside.maxConns"]["value"]}')

Explanation
-----------

| This is simlar to tmsh show command.
| If the object properties includes another dictionary, keep adding keys until you find the value you need.
| In this example "clientside.maxConns" property has a dictionary, and we want the value of the key "value".