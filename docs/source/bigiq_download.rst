download
========

Code
----

.. automethod:: bigrest.bigiq.BIGIQ.download

Example
-------

.. code-block:: python

    device.download(
        "/mgmt/shared/file-transfer/uploads", "bigrest.iso")

Explanation
-----------

| This downloads a file from the device.
| The API limit downloads to chunks of 1M, so BIGREST will handle that.
| You just need to pass the HTTP path to upload and the local file.

| I am only aware of one location from where you can download files from BIG-IQ.


| **Folder:** /var/config/rest/downloads
| **HTTP path:** /mgmt/shared/file-transfer/uploads

| **/var/config/rest/downloads** is the folder created for iControl REST API downloads and uploads.