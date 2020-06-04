download
========

Code
----

.. automethod:: bigrest.bigip.BIGIP.download

Example
-------

.. code-block:: python

    device.download(
        "/mgmt/shared/file-transfer/downloads", "bigrest.iso")

Explanation
-----------

| This downloads a file from the device.
| The API limit downloads to chunks of 1M, so BIGREST will handle that.
| You just need to pass the HTTP path to upload and the local file.

| I am only aware of 2 locations from where you can download files from BIG-IP.


| **Folder:** /var/config/rest/downloads/tmp-access/
| **HTTP path:** /mgmt/shared/file-transfer/downloads

| **Folder:** /shared/images
| **HTTP path:** /mgmt/cm/autodeploy/software-image-downloads

| **/var/config/rest/downloads** is the folder created for iControl REST API downloads and uploads.
| While **/shared/images** is where we have software images.