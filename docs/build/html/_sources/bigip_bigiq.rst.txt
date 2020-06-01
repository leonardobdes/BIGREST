BIG-IP API vs BIG-IQ API
========================

| Majority of the F5 iControl REST API functionalities are the same for both BIG-IP and BIG-IQ.
| However, some major differences exist, so BIGREST treats BIG-IP and BIG-IQ devices different.
| For BIG-IP use the class BIGIP, for BIG-IQ use the class BIGIQ.

BIG-IP
------

**TOC**

When using BIGREST for a BIG-IP device, the simplest way to find out the HTTP path you need is to use the TOC.

To access TOC:

.. code-block::

   https://<hostname or IP>/mgmt/toc

**API Discovery**

| If you query root HTTP path of the API, it will show you all HTTP paths available.
| Example:

.. code-block::

   GET https://<hostname or IP>/mgmt/tm

| Also, you can also query a HTTP path to see the next paths available.

.. code-block::

   GET https://<hostname or IP>/mgmt/tm/ltm

See the documentation section for a full list of HTTP paths.

**API**

| BIG-IP API use is simpler than BIG-IQ API.
| Majority of the HTTP paths starts with **/mgmt/tm/**.

| There are also some HTTP paths that I guess were create to be used by BIG-IQ when managing a BIG-IP device.
| Those HTTP paths start with **/mgmt/cm/**.

HTTP paths for functionality that is specific to the iControl REST API starts with **/mgmt/shared/**

| The API is similar to tmsh commands.
| If you want to list all virtual servers using tmsh you do:

.. code-block::

   tmsh list ltm virtual

If you want list all virtual servers using the API, you do:

.. code-block::

   GET https://<hostname or IP>/mgmt/tm/ltm/virtual

If you want to list a single virtual server using tmsh you do:

.. code-block::

   tmsh list ltm virtual <virtual server name>

If you want to list a single virtual server using the API you do:

.. code-block::

   GET https://<hostname or IP>/mgmt/tm/ltm/virtual/<virtual server name>

**Documentation**

| F5 site:
| https://clouddocs.f5.com/api/icontrol-rest/

| iControl REST User Guide provides a good explanation about the API:
| https://cdn.f5.com/websites/devcentral.f5.com/downloads/icontrol-rest-api-user-guide-14-1-0.pdf
| At the time I am writing this documentation, 14.1.0 is the lastest version for this guide, but 15.1.0 is the latest BIG-IP version.

| This askf5 solution provides many examples:
| https://support.f5.com/csp/article/K13225405

| Full list of HTTP paths for **/mgmt/tm** in 15.1.0:
| https://raw.githubusercontent.com/leonardobdes/BIGREST/master/api/bigip_mgmt_tm_15_1_0.txt

| Full list of HTTP paths for **/mgmt/cm** in 15.1.0:
| https://raw.githubusercontent.com/leonardobdes/BIGREST/master/api/bigip_mgmt_cm_15_1_0.txt

| Full list of HTTP paths for **/mgmt/shared** in 15.1.0:
| https://raw.githubusercontent.com/leonardobdes/BIGREST/master/api/bigip_mgmt_shared_15_1_0.txt

BIG-IQ
------

**TOC**

BIG-IQ does not have TOC.

**API Discovery**

| If you query root HTTP path of the API, it will show you all HTTP paths available.
| Example:

.. code-block::

   GET https://<hostname or IP>/mgmt/cm

| Unfortunally, BIG-IQ does not implement next HTTP paths for all paths, so the following does not work in BIG-IQ.

.. code-block::

   GET https://<hostname or IP>/mgmt/cm/adc-core/working-config/ltm

See the documentation section for a full list of HTTP paths.

**API**

| A BIG-IQ device provides a subset of the BIG-IP functionality, plus functionality that is specific to BIG-IQ.
| For example you can list the self IPs in both BIG-IQ and BIG-IP using the following tmsh command:

.. code-block::

   tmsh list net self

| This means that the majority of the HTTP path you use in the BIG-IP API for the device itself will also work with BIG-IQ.
| Those HTTP paths will start with **/mgmt/tm/**.

HTTP paths to work BIG-IQ functionalities start with **/mgmt/cm/**.

HTTP paths for functionality that is specific to the iControl REST API starts with **/mgmt/shared/**

| The API is similar to tmsh commands.
| However, BIG-IQ only has tmsh commands that are specific to the BIG-IQ itself.
| If you want list all virtual servers using the API, you do:

.. code-block::

   GET https://<hostname or IP>/mgmt/cm/adc-core/working-config/ltm/virtual

| BIG-IQ is a very new products compated with BIG-IP, however, it had many major changes since it was created.
| The adc-core name is the same as LTM, and I assume it is a legacy from the time BIG-IQ had separated products.

| Instead of using the object name as the key to get that object, BIG-IQ API uses IDs.
| If you want to list a single virtual server using the API you do:

.. code-block::

   GET https://<hostname or IP>/mgmt/tm/ltm/virtual/<ID>

| This means you need to know the ID, or you have to get the ID before.
| The SDK has a function called "id" to help with that.

| BIG-IQ API also requires you to provide a link to a object in some cases.
| For example, if you create a virtual server, you have to provide a link device.
| The link is sent as part of the payload, and means the virtual server will be linked to that device.
| The SDK has a function called "link" to help with that.

**Documentation**

| F5 site:
| https://clouddocs.f5.com/products/big-iq/mgmt-api/latest/

| BIG-IQ API does not have a user guide like BIG-IP, but the API Reference provides similar content.
| https://clouddocs.f5.com/products/big-iq/mgmt-api/latest/ApiReferences/bigiq_public_api_ref/r_public_api_references.html

| This part of the documentation provides many examples:
| https://clouddocs.f5.com/products/big-iq/mgmt-api/latest/HowToSamples/bigiq_public_api_wf/t_bigiq_public_api_workflows.html

| List of HTTP paths for **/mgmt/tm** in 7.1.0:
| https://raw.githubusercontent.com/leonardobdes/BIGREST/master/api/bigiq_mgmt_tm_15_1_0.txt
| BIG-IQ does not display the full list, so use BIG-IP list below as reference:
| https://raw.githubusercontent.com/leonardobdes/BIGREST/master/api/bigip_mgmt_tm_15_1_0.txt

| Full list of HTTP paths for **/mgmt/cm** in 7.1.0:
| https://raw.githubusercontent.com/leonardobdes/BIGREST/master/api/bigiq_mgmt_cm_15_1_0.txt

| Full list of HTTP paths for **/mgmt/shared** in 7.1.0:
| https://raw.githubusercontent.com/leonardobdes/BIGREST/master/api/bigiq_mgmt_shared_15_1_0.txt