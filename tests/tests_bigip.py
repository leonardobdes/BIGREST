"""
BIGREST SDK tests
Perform test on a BIG-IP device
"""

# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import getpass
import os
import hashlib

# Internal imports
# Import only with "from x import y", to simplify the code.
from ..bigrest.bigip import BIGIP
from ..bigrest.utils.utils import rest_format
from ..bigrest.utils.utils import token

# Get username, password, and ip
print("Username: ", end="")
username = input()
password = getpass.getpass()
print("Device IP or name: ", end="")
ip = input()

# Create a device object with basic authentication
device = BIGIP(ip, username, password)

# Objects list
pool_name = "/bigrest/bigrest_pool"
node_name = "/bigrest/172.17.0.1"
member_name = "/bigrest/172.17.0.1:80"
partition_name = "/bigrest"
virtual_name = "/bigrest/bigrest_vs"
virtual_name2 = "/bigrest/bigrest_vs2"
pool_name2 = "/bigrest/bigrest_pool2"
virtual_name3 = "/bigrest/bigrest_vs3"
pool_name3 = "/bigrest/bigrest_pool3"
scf_name = "bigrest.scf"
filename = "bigrest.iso"

# Create folder
data = {}
data["name"] = "bigrest"
data["partition"] = "/"
partition = device.create("/mgmt/tm/sys/folder", data)
if partition.properties["fullPath"] != partition_name:
    raise Exception(partition.properties["fullPath"])
else:
    print(f"Partition {partition_name} created.")

# Create pool
data = {}
data["name"] = pool_name
pool = device.create("/mgmt/tm/ltm/pool", data)
if pool.properties["fullPath"] != pool_name:
    raise Exception(pool.properties["fullPath"])
else:
    print(f"Pool {pool_name} created.")

# Add pool member
data = {}
data["name"] = member_name
member = device.create(
    f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members", data)
if member.properties["fullPath"] != "/bigrest/172.17.0.1:80":
    raise Exception(member.properties["fullPath"])
else:
    print(f"Member {member_name} created.")

# Add virtual server
data = {}
data["name"] = virtual_name
data["destination"] = "10.17.0.1%0:80"
virtual = device.create("/mgmt/tm/ltm/virtual", data)
if virtual.properties["fullPath"] != virtual_name:
    raise Exception(virtual.properties["fullPath"])
else:
    print(f"Virtual {virtual_name} created.")

# Add pool to virtual server
virtual = device.load(
    f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}")[0]
virtual.properties["pool"] = pool_name
virtual_updated = device.save(virtual)
if virtual_updated.properties["pool"] != pool_name:
    raise Exception(virtual_updated.properties["pool_name"])
else:
    print(f"Virtual {virtual_name} modified.")

# Print virtual servers name
virtuals = device.load("/mgmt/tm/ltm/virtual")
print("List all virtual servers:")
for virtual in virtuals:
    print(virtual.properties["name"])

# Print node
node = device.load(f"/mgmt/tm/ltm/node/{rest_format(node_name)}")[0]
print("Print node:")
print(node)

# Print node example
node = device.example(f"/mgmt/tm/ltm/node")
print("Print node example:")
print(node)

# Modify pool description
data = {}
description = "bigrest"
data["description"] = description
pool_updated = device.modify(
    f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}", data)
if pool_updated.properties["description"] != description:
    raise Exception(pool_updated.properties["description"])
else:
    print(f"Pool {virtual_name} modified.")

# Test if virtual server exists
if device.exist(f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}"):
    print(f"Virtual {virtual_name} exists.")
else:
    raise Exception(f"Error testing if {virtual_name} exists.")
fake_virtual_name = "/Common/fake"
if device.exist(f"/mgmt/tm/ltm/virtual/{rest_format(fake_virtual_name)}"):
    raise Exception(f"Error testing if {fake_virtual_name} exists.")
else:
    print(f"Virtual {fake_virtual_name} does not exist.")

# Show virtual server information
virtual = device.show(
    f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}")[0]
max_conns = virtual.properties["clientside.maxConns"]["value"]
if max_conns != 0:
    raise Exception(max_conns)
else:
    print(f"Virtual {virtual_name} maximum number of connections.")

# Test transaction
transaction_create = device.transaction_create()
transaction_id = transaction_create.properties["transId"]
print(f"Transaction ID: {transaction_id}.")
data = {}
data["name"] = pool_name2
device.create("/mgmt/tm/ltm/pool", data)
data = {}
data["name"] = virtual_name2
data["destination"] = "10.17.0.2%0:80"
device.create("/mgmt/tm/ltm/virtual", data)
device.transaction_validate()
device.transaction_commit()
print(f"Transaction {transaction_id} completed.")

# Test transaction with "with"
with device as transaction:
    data = {}
    data["name"] = pool_name3
    device.create("/mgmt/tm/ltm/pool", data)
    data = {}
    data["name"] = virtual_name3
    data["destination"] = "10.17.0.3%0:80"
    device.create("/mgmt/tm/ltm/virtual", data)
print('Transaction with "with" completed.')

# Test transaction functions
transaction_create = device.transaction_create()
transaction_id = transaction_create.properties["transId"]
print(f"Transaction ID: {transaction_id}.")
data = {}
data["name"] = pool_name2
device.create("/mgmt/tm/ltm/pool", data)
data = {}
data["name"] = virtual_name2
data["destination"] = "10.17.0.2%0:80"
device.create("/mgmt/tm/ltm/virtual", data)
try:
    device.transaction_validate()
    raise Exception("Transaction should have failed.")
except Exception:
    print("Transaction validated.")

# Test command
data = {}
data["command"] = "run"
data["utilCmdArgs"] = "-c 'cat /VERSION'"
result = device.command("/mgmt/tm/util/bash", data)
if "BIG-IP" in result:
    print("Bash command tested.")
else:
    raise Exception(result)

# Test task
data = {}
data["command"] = "save"
task = device.task_start("/mgmt/tm/task/sys/config", data)
device.task_wait(task)
if device.task_completed(task):
    device.task_result(task)
    print("Task test completed.")
else:
    raise Exception()

# Test upload and download
with open(filename, "wb") as file_:
    file_.write(os.urandom(10485760))
with open(filename, "rb") as file_:
    file_hash = hashlib.md5()
    file_hash.update(file_.read())
    md5_original = file_hash.hexdigest()
device.upload(
    "/mgmt/cm/autodeploy/software-image-uploads", filename=filename)
os.remove(filename)
device.download(
    f"/mgmt/cm/autodeploy/software-image-downloads", filename=filename)
with open(filename, "rb") as file_:
    file_hash = hashlib.md5()
    file_hash.update(file_.read())
    md5_new = file_hash.hexdigest()
if md5_original == md5_new:
    print("Upload and download tests completed.")
else:
    raise Exception("Different md5s.")

# Create a device object with basic authentication and request_token
device = BIGIP(ip, username, password, request_token=True)

# Create a device object to use token
token_ = token(ip, username, password)
device = BIGIP(ip, token=token_)

# Delete pool member
path = (
    f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}"
    f"/members/{rest_format(member_name)}"
)
device.delete(path)
print(f"Member {member_name} deleted.")

# Delete node
device.delete(f"/mgmt/tm/ltm/node/{rest_format(node_name)}")
print(f"Node {node_name} deleted.")

# Delete virtual
device.delete(f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}")
print(f"Virtual {virtual_name} deleted.")

# Delete virtual
device.delete(f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name2)}")
print(f"Virtual {virtual_name2} deleted.")

# Delete virtual
device.delete(f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name3)}")
print(f"Virtual {virtual_name3} deleted.")

# Delete pool
device.delete(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}")
print(f"Pool {pool_name} deleted.")

# Delete pool
device.delete(f"/mgmt/tm/ltm/pool/{rest_format(pool_name2)}")
print(f"Pool {pool_name2} deleted.")

# Delete pool
device.delete(f"/mgmt/tm/ltm/pool/{rest_format(pool_name3)}")
print(f"Pool {pool_name3} deleted.")

# Delete partition
device.delete(f"/mgmt/tm/sys/folder/{rest_format(partition_name)}")
print(f"Partition {partition_name} deleted.")

# Remove local file
os.remove(filename)
print(f"Local file {filename} deleted.")

# Remove remote file
data = {}
data["command"] = "run"
data["utilCmdArgs"] = f"-c 'rm -I /shared/images/{filename}'"
device.command("/mgmt/tm/util/bash", data)
print(f"Remote file {filename} deleted.")
