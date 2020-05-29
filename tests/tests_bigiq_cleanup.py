"""
BIGREST SDK tests
Delete objects created during tests for BIG-IQ
"""

# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import getpass
import os

# BIGREST Imports
# Import only with "from x import y", to simplify the code.
from ..bigrest.bigiq import BIGIQ

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
virtual_name2 = "bigrest_vs2"
pool_name2 = "bigrest_pool2"
virtual_name3 = "bigrest_vs3"
pool_name3 = "bigrest_pool3"
scf_name = "bigrest.scf"
filename = "bigrest.iso"

# Delete pool member
try:
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/pool"
        f"?$filter=name eq '{pool_name}'"
    )
    pool_id = device.id(path)
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/pool"
        f"/{pool_id}/members?$filter=name eq '{member_name}'"
    )
    member_id = device.id(path)
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/pool"
        f"/{pool_id}/members/{member_id}"
    )
    device.delete(path)
    print(f"Member {member_name} deleted.")
except Exception:
    print(f"Member {member_name} not found.")

# Delete node
try:
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/node"
        f"?$filter=name eq '{node_name}'"
    )
    node_id = device.id(path)
    device.delete(f"/mgmt/cm/adc-core/working-config/ltm/node/{node_id}")
    print(f"Node {node_name} deleted.")
except Exception:
    print(f"Node {node_name} not found.")

# Delete virtual
try:
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/virtual"
        f"?$filter=name eq '{virtual_name}'"
    )
    virtual_id = device.id(path)
    device.delete(
        f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id}")
    print(f"Virtual {virtual_name} deleted.")
except Exception:
    print(f"Virtual {virtual_name} not found.")

# Delete virtual
try:
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/virtual"
        f"?$filter=name eq '{virtual_name2}'"
    )
    virtual_id2 = device.id(path)
    device.delete(
        f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id2}")
    print(f"Virtual {virtual_name2} deleted.")
except Exception:
    print(f"Virtual {virtual_name2} not found.")

# Delete virtual
try:
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/virtual"
        f"?$filter=name eq '{virtual_name3}'"
    )
    virtual_id3 = device.id(path)
    device.delete(
        f"/mgmt/cm/adc-core/working-config/ltm/virtual/{virtual_id3}")
    print(f"Virtual {virtual_name3} deleted.")
except Exception:
    print(f"Virtual {virtual_name3} not found.")

# Delete pool
try:
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/pool"
        f"?$filter=name eq '{pool_name}'"
    )
    pool_id = device.id(path)
    device.delete(f"/mgmt/cm/adc-core/working-config/ltm/pool/{pool_id}")
    print(f"Pool {pool_name} deleted.")
except Exception:
    print(f"Pool {pool_name} not found.")

# Delete pool
try:
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/pool"
        f"?$filter=name eq '{pool_name2}'"
    )
    pool_id2 = device.id(path)
    device.delete(f"/mgmt/cm/adc-core/working-config/ltm/pool/{pool_id2}")
    print(f"Pool {pool_name2} deleted.")
except Exception:
    print(f"Pool {pool_name2} not found.")

# Delete pool
try:
    path = (
        f"/mgmt/cm/adc-core/working-config/ltm/pool"
        f"?$filter=name eq '{pool_name3}'"
    )
    pool_id3 = device.id(path)
    device.delete(
        f"/mgmt/cm/adc-core/working-config/ltm/pool/{pool_id3}")
    print(f"Pool {pool_name3} deleted.")
except Exception:
    print(f"Pool {pool_name3} not found.")

# Remove local file
try:
    os.remove(filename)
    print(f"Local file {filename} deleted.")
except Exception:
    print(f"Local file {filename} not found.")

# Remove remote file
try:
    data = {}
    data["command"] = "run"
    data["utilCmdArgs"] = "/var/config/rest/downloads/bigrest.iso"
    result = device.command("/mgmt/tm/util/unix-rm", data)
    print(f"Remote file {filename} deleted.")
except Exception:
    print(f"Remote file {filename} not found.")

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

# Remove config from devices
data = {
   "name": "BIGREST remove config from device",
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
