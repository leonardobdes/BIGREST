"""
BIGREST SDK tests
Perform test on a BIG-IQ device
"""

# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import getpass
import os
import hashlib

# Internal imports
# Import only with "from x import y", to simplify the code.
from ..bigrest.bigiq import BIGIQ
from ..bigrest.utils.utils import token
from ..bigrest.utils.utils import refresh_token

# Get username, password, and ip
print("Username: ", end="")
username = input()
password = getpass.getpass()
print("Device IP or name: ", end="")
ip = input()

# Create a device object with basic authentication
device = BIGIQ(ip, username, password)

# Objects list
device_name = "LABBIGIP1.lab.local"
device_name2 = "LABBIGIP2.lab.local"
pool_name = "bigrest_pool"
node_name = "172.17.0.1"
member_name = "172.17.0.1:80"
partition_name = "Common"
virtual_name = "bigrest_vs"
scf_name = "bigrest.scf"
filename = "bigrest.iso"

# Get device link
path = (
    f"/mgmt/shared/resolver/device-groups/cm-adccore-allbigipDevices/devices"
    f"?$filter=hostname eq '{device_name}'"
)
device_link = device.link(path)
path = (
    f"/mgmt/shared/resolver/device-groups/cm-adccore-allbigipDevices/devices"
    f"?$filter=hostname eq '{device_name2}'"
)
device_link2 = device.link(path)

# Create node
data = {
    "partition": f"{partition_name}",
    "name": f"{node_name}",
    "address": "172.17.0.1",
    "deviceReference": {
        "link": device_link
    }
}
node = device.create(
    "/mgmt/cm/adc-core/working-config/ltm/node", data)
node_id = node.properties["id"]
node_link = node.properties["selfLink"]
if node.properties["name"] != node_name:
    raise Exception(node.properties["name"])
else:
    print(f"Node {node_name} created.")

# Create Pool
data = {
    "partition": f"{partition_name}",
    "name": f"{pool_name}",
    "deviceReference": {
        "link": device_link
    }
}
pool = device.create(
    "/mgmt/cm/adc-core/working-config/ltm/pool", data)
pool_id = pool.properties["id"]
pool_link = pool.properties["selfLink"]
if pool.properties["name"] != pool_name:
    raise Exception(pool.properties["name"])
else:
    print(f"Pool {pool_name} created.")

# Add pool member
data = {
    "partition": f"{partition_name}",
    "name": f"{member_name}",
    "port": 80,
    "nodeReference": {
        "link": node_link
    }
}
path = (
    f"/mgmt/cm/adc-core/working-config/ltm/pool"
    f"/{pool_id}/members"
)
member = device.create(path, data)
member_id = member.properties["id"]
if member.properties["name"] != member_name:
    raise Exception(member.properties["name"])
else:
    print(f"Member {member_name} created.")

# Create virtual
data = {
    "partition": f"{partition_name}",
    "name": f"{virtual_name}",
    "destinationAddress": "10.17.0.1",
    "mask": "255.255.255.255",
    "destinationPort": 80,
    "sourceAddress": "0.0.0.0/0",
    "deviceReference": {
        "link": device_link
    }
}
virtual = device.create(
    f"/mgmt/cm/adc-core/working-config/ltm/virtual", data)
virtual_id = virtual.properties["id"]
if virtual.properties["name"] != virtual_name:
    raise Exception(virtual.properties["name"])
else:
    print(f"Virtual {virtual_name} created.")

# Add pool to virtual server
virtual = device.load(
    f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id}")[0]
virtual.properties["poolReference"] = {"link": f"{pool_link}"}
virtual_updated = device.save(virtual)
if virtual_updated.properties["poolReference"]["name"] != pool_name:
    raise Exception(virtual_updated.properties["poolReference"]["name"])
else:
    print(f"Virtual {virtual_name} modified.")

# Deploy configuration - task test
data = {
   "name": "BIGREST Add config to device",
   "deviceReferences": [
        {
            "link": device_link
        },
        {
            "link": device_link2
        }
   ],
   "disableUnusedObjectRemoval": True
}
task = device.task_start(
    "/mgmt/cm/adc-core/tasks/deploy-configuration", data)
device.task_wait(task)
if device.task_completed(task):
    print("Task test completed.")
else:
    raise Exception()

# Print virtual servers name
virtuals = device.load("/mgmt/cm/adc-core/working-config/ltm/virtual")
print("List all virtual servers:")
for virtual in virtuals:
    print(virtual.properties["deviceReference"]["name"])
    print(virtual.properties["name"])

# Print node
node = device.load(
    f"/mgmt/cm/adc-core/working-config/ltm/node/{node_id}")[0]
print("Print node:")
print(node)

# Print node example
node = device.example(f"/mgmt/cm/adc-core/working-config/ltm/node")
print("Print node example:")
print(node)

# Modify pool description
data = {}
description = "bigrest"
data["description"] = description
pool_updated = device.modify(
    f"/mgmt/cm/adc-core/working-config/ltm/pool/{pool_id}", data)
if pool_updated.properties["description"] != description:
    raise Exception(pool_updated.properties["description"])
else:
    print(f"Pool {virtual_name} modified.")

# Test if virtual server exists
path = (
    f"/mgmt/cm/adc-core/working-config/ltm/virtual"
    f"?$filter=name eq '{virtual_name}'"
)
if device.exist(path):
    print(f"Virtual {virtual_name} exists.")
else:
    raise Exception(f"Error testing if {virtual_name} exists.")
fake_virtual_name = "/Common/fake"
path = (
    f"/mgmt/cm/adc-core/working-config/ltm/virtual"
    f"?$filter=name eq '{fake_virtual_name}'"
)
if device.exist(path):
    raise Exception(f"Error testing if {fake_virtual_name} exists.")
else:
    print(f"Virtual {fake_virtual_name} does not exist.")

# Show virtual server information
virtual = device.show(
    f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id}")[0]
virtual_availability = virtual.properties[
    "status.availabilityState"]["description"]
if virtual_availability != "unknown":
    raise Exception(virtual_availability)
else:
    print(f"Virtual {virtual_name} availability.")

# Test transaction
# BIG-IQ does not support transactions

# Test command
data = {}
data["command"] = "run"
data["utilCmdArgs"] = "-c1 localhost"
result = device.command("/mgmt/tm/util/ping", data)
if "1 received" in result:
    print("Ping command tested.")
else:
    raise Exception(result)

# Test upload and download
with open(filename, "wb") as file_:
    file_.write(os.urandom(10485760))
with open(filename, "rb") as file_:
    file_hash = hashlib.md5()
    file_hash.update(file_.read())
    md5_original = file_hash.hexdigest()
device.upload("/mgmt/shared/file-transfer/uploads", filename=filename)
os.remove(filename)
data = {}
data["command"] = "run"
data["utilCmdArgs"] = ("/var/config/rest/downloads/bigrest.iso "
                       "/var/config/rest/downloads/tmp-access/")
device.command("/mgmt/tm/util/unix-mv", data)
device.download(
    f"/mgmt/shared/file-transfer/downloads", filename=filename)
with open(filename, "rb") as file_:
    file_hash = hashlib.md5()
    file_hash.update(file_.read())
    md5_new = file_hash.hexdigest()
if md5_original == md5_new:
    print("Upload and download tests completed.")
else:
    raise Exception("Different md5s.")

# Create a device object with basic authentication and request_token
device = BIGIQ(ip, username, password, request_token=True)

# Create a device object to use token
token_ = token(ip, username, password)
device = BIGIQ(ip, username, password, token=token_)

# Create a device object to use refresh token
refresh_token_ = refresh_token(ip, username, password)
device = BIGIQ(ip, refresh_token=refresh_token_)

# Delete pool member
path = (
    f"/mgmt/cm/adc-core/working-config/ltm/pool"
    f"/{pool_id}/members/{member_id}"
)
device.delete(path)
print(f"Member {member_name} deleted.")

# Delete node
device.delete(f"/mgmt/cm/adc-core/working-config/ltm/node/{node_id}")
print(f"Node {node_name} deleted.")

# Delete virtual
device.delete(
    f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id}")
print(f"Virtual {virtual_name} deleted.")

# Delete pool
device.delete(f"/mgmt/cm/adc-core/working-config/ltm/pool/{pool_id}")
print(f"Pool {pool_name} deleted.")

# Remove local file
os.remove(filename)
print(f"Local file {filename} deleted.")

# Remove remote file
data = {}
data["command"] = "run"
data["utilCmdArgs"] = "/var/config/rest/downloads/bigrest.iso"
result = device.command("/mgmt/tm/util/unix-rm", data)
print(f"Remote file {filename} deleted.")

# Remove configuration
data = {
   "name": "BIGREST remove config to device",
   "deviceReferences": [
        {
            "link": device_link
        },
        {
            "link": device_link2
        }
   ],
   "disableUnusedObjectRemoval": True
}
task = device.task_start(
    "/mgmt/cm/adc-core/tasks/deploy-configuration", data)
device.task_wait(task)
if device.task_completed(task):
    print("Task test completed.")
else:
    raise Exception()
