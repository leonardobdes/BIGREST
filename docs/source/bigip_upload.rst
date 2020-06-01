upload
======

Code
----

.. automethod:: bigrest.bigip.BIGIP.upload

Example
-------

.. code-block:: python

    device.upload(
        "/mgmt/cm/autodeploy/software-image-uploads", "bigrest.iso")

Explanation
-----------

| This upload the local file to the device.
| The API limits uploads to chunks of 1M, so BIGREST will handle that.
| You just need to pass the HTTP path to the location to upload, and the local file.

| I am only aware of 2 locations that you can upload files to BIG-IP.


| Folder: /var/config/rest/downloads
| HTTP path: /mgmt/shared/file-transfer/uploads
| Folder: /shared/images
| HTTP path: /mgmt/cm/autodeploy/software-image-uploads

| /var/config/rest/downloads is the folder create for iControl REST API downloads and uploads.
| While /shared/images is where we have software images.