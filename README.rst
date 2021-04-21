What is BIGREST?
----------------

| F5 BIG-IP and BIG-IQ devices have an API called iControl REST.
| BIGREST is an SDK with multiple methods and functions that simplifies the use of the iControl REST API.

What is useful for?
-------------------

| If you want to automate tasks on a BIG-IP or BIG-IQ devices, one of the options is to use the iControl REST API.
| If you interact with the API directly, you will have to know how the API works, including headers, tokens, etc...
| Probably, you will end up scripting those tasks using a programming language, and creating some functions you normally use.

| BIGREST removes that work, as it includes those functions that you normally use.
| It creates a kind of abstraction layer on to of the API.

Why create another SDK?
-----------------------

| This was one of the first questions I got when BIGREST was released.
| In case you don't know, there was already an SDK (https://github.com/F5Networks/f5-common-python) before BIGREST was created.

| I have used the other SDK, and I did initially wanted to support and expand it.
| However, the approach that was taken in that SDK to defined every HTTP path as Python modules made it difficult to expand and support it.
| For example, it just supports very few BIG-IQ functionalities.

| On the other hand, BIGREST tries to be more generic as possible, and the user has to indicate the HTTP path they want to use.
| This means any new HTTP path included on the next version will be automatically available on BIGREST.
| Also, with this generic approach, it fully supports both BIG-IP and BIG-IQ.

BIGREST functionalities
-----------------------

- Supports partition
- Supports route domain
- Support HTTP basic authentication
- Support token
- Support refresh token
- Implements all HTTP methods used in the iControl REST API
- Implements HTTP path /stats
- Implements HTTP path /example
- Implements command
- Implements task
- Implements transaction

Documentation
-------------

https://bigrest.readthedocs.io/

Source code
-------------

https://github.com/leonardobdes/BIGREST

Author
------

| **Name:**
| Leonardo Souza

| **LinkedIn:**
| https://uk.linkedin.com/in/leonardobdes

Contributor
------------

| **Name:**
| Jason Rahm

| **LinkedIn:**
| https://www.linkedin.com/in/jrahm

How to install?
---------------

**Requires Python version 3.7**

Install BIGREST using Python **pip**:

.. code-block:: python

   pip install bigrest

How to use it?
---------------

**In the following example:**

:192.168.1.245:
    IP or name of the F5 device.
:admin:
    Username to be used to connect to the device.
:password:
    Password to be used to connect to the device.

**First, import the SDK:**

.. code-block:: python

   from bigrest.bigip import BIGIP

**Next, create a device object:**

.. code-block:: python

   device = BIGIP("192.168.1.245", "admin", "password")

**Lastily, load all virtual servers and print their names:**

.. code-block:: python

    virtuals = device.load("/mgmt/tm/ltm/virtual")
    for virtual in virtuals:
        print(virtual.properties["name"])

| This is just a simple example to give you a first view about the SDK.
| Detailed information about how to use the SDK will be provided in the next sections of this documentation.

How to get help?
----------------

If you have problems using this SDK, or to understand how the F5 iControl REST API works, use `DevCentral <https://devcentral.f5.com/>`_ website to get help.

How to report bugs?
-------------------

| Use `GitHub <https://github.com/leonardobdes/BIGREST/issues>`_ issues to report bugs.
| For any bug, please provide the following information.

BIGREST version:**

Run the following command to find the version you are using.

.. code-block:: python

   pip show bigrest

**F5 device type:**

BIG-IP or BIG-IQ

**F5 device version:**

Run the following command to find the version you are using.

.. code-block:: python

   tmsh show sys version

**Python code to replicate the bug.**

**Output generated when the bug is triggered.**

How to request new functionalities?
-----------------------------------

| Use `GitHub <https://github.com/leonardobdes/BIGREST/issues>`_ issues to request new functionalities.
| Use the following format in the title **RFE - Title**.