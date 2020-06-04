F5 Known Issues
===============

| There are some F5 known issues that will affect the use of the BIGREST SDK.
| However, these are known issues of the iControl REST API and not BIGREST SDK.
| Whenever possible a workaround will be created, but in some cases it is not possible.

Saving UCS backup through iControl REST fails with TimeoutException
-------------------------------------------------------------------

Link
~~~~
https://cdn.f5.com/product/bugtracker/ID797721.html


BIGREST workaround
~~~~~~~~~~~~~~~~~~

None.

Cannot download files larger than 32MB via iControl REST
--------------------------------------------------------

Link
~~~~
https://cdn.f5.com/product/bugtracker/ID516683.html


BIGREST workaround
~~~~~~~~~~~~~~~~~~

BIGREST only downloads chunks of 1M each time.