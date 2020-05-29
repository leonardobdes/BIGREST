"""
BIGREST SDK tests
Delete objects created during tests for BIG-IP
"""

# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import getpass
import os

# Internal imports
# Import only with "from x import y", to simplify the code.
from ..bigrest.bigip import BIGIP
from ..bigrest.utils.utils import rest_format

# Get username, password, and ip
print("Username: ", end="")
username = input()
password = getpass.getpass()
print("Device IP or name: ", end="")
ip = input()

# Create a device object
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

# Delete pool member
try:
    path = (
        f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}"
        f"/members/{rest_format(member_name)}"
    )
    device.delete(path)
    print(f"Member {member_name} deleted.")
except Exception:
    print(f"Member {member_name} not found.")

# Delete node
try:
    device.delete(f"/mgmt/tm/ltm/node/{rest_format(node_name)}")
    print(f"Node {node_name} deleted.")
except Exception:
    print(f"Node {node_name} not found.")

# Delete virtual
try:
    device.delete(f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}")
    print(f"Virtual {virtual_name} deleted.")
except Exception:
    print(f"Virtual {virtual_name} not found.")

# Delete virtual
try:
    device.delete(f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name2)}")
    print(f"Virtual {virtual_name2} deleted.")
except Exception:
    print(f"Virtual {virtual_name2} not found.")

# Delete virtual
try:
    device.delete(f"/mgmt/tm/ltm/virtual/{rest_format(virtual_name3)}")
    print(f"Virtual {virtual_name3} deleted.")
except Exception:
    print(f"Virtual {virtual_name3} not found.")

# Delete pool
try:
    device.delete(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}")
    print(f"Pool {pool_name} deleted.")
except Exception:
    print(f"Pool {pool_name} not found.")

# Delete pool
try:
    device.delete(f"/mgmt/tm/ltm/pool/{rest_format(pool_name2)}")
    print(f"Pool {pool_name2} deleted.")
except Exception:
    print(f"Pool {pool_name2} not found.")

# Delete pool
try:
    device.delete(f"/mgmt/tm/ltm/pool/{rest_format(pool_name3)}")
    print(f"Pool {pool_name3} deleted.")
except Exception:
    print(f"Pool {pool_name3} not found.")

# Delete partition
try:
    device.delete(f"/mgmt/tm/sys/folder/{rest_format(partition_name)}")
    print(f"Folder {partition_name} deleted.")
except Exception:
    print(f"Folder {partition_name} not found.")

# Remove local file
try:
    os.remove(filename)
    print(f"Local file {filename} deleted.")
except Exception:
    print(f"Local file {filename} not found.")

# Remove remote file
data = {}
data["command"] = "run"
data["utilCmdArgs"] = f"-c 'rm -I /shared/images/{filename}'"
result = device.command("/mgmt/tm/util/bash", data)
if result == "":
    print(f"Remote file {filename} deleted.")
else:
    print(f"Remote file {filename} not found.")
