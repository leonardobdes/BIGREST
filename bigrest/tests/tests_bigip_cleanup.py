"""
BIGREST SDK tests
Delete objects created during tests
"""

# External Imports
# Import only with 'import package',
# it will make explicity in the code where it came from.
import getpass

# BIGREST Imports
# Import only with 'from x import y', to simplify the code.
from ..bigrest import BIGREST
from ..utils.utils import rest_format

# Get username, password, and ip
print('Username: ', end='')
username = input()
password = getpass.getpass()
print('Device IP or name: ', end='')
ip = input()

# Create a device object
device = BIGREST(device=ip, username=username, password=password)

# Objects list
pool_name = '/bigrest/bigrest_pool'
node_name = '/bigrest/172.17.0.1'
member_name = '/bigrest/172.17.0.1:80'
partition_name = '/bigrest'
virtual_name = '/bigrest/bigrest_vs'
virtual_name2 = '/bigrest/bigrest_vs2'
pool_name2 = '/bigrest/bigrest_pool2'
virtual_name3 = '/bigrest/bigrest_vs3'
pool_name3 = '/bigrest/bigrest_pool3'

# Delete pool member
try:
    device.delete(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(member_name)}')
    print(f'Member {member_name} deleted.')
except Exception:
    print(f'Member {member_name} not found.')

# Delete node
try:
    device.delete(path=f'/mgmt/tm/ltm/node/{rest_format(node_name)}')
    print(f'Node {node_name} deleted.')
except Exception:
    print(f'Node {node_name} not found.')

# Delete virtual
try:
    device.delete(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}')
    print(f'Virtual {virtual_name} deleted.')
except Exception:
    print(f'Virtual {virtual_name} not found.')

# Delete virtual
try:
    device.delete(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name2)}')
    print(f'Virtual {virtual_name2} deleted.')
except Exception:
    print(f'Virtual {virtual_name2} not found.')

# Delete virtual
try:
    device.delete(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name3)}')
    print(f'Virtual {virtual_name3} deleted.')
except Exception:
    print(f'Virtual {virtual_name3} not found.')

# Delete pool
try:
    device.delete(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}')
    print(f'Pool {pool_name} deleted.')
except Exception:
    print(f'Pool {pool_name} not found.')

# Delete pool
try:
    device.delete(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name2)}')
    print(f'Pool {pool_name2} deleted.')
except Exception:
    print(f'Pool {pool_name2} not found.')

# Delete pool
try:
    device.delete(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name3)}')
    print(f'Pool {pool_name3} deleted.')
except Exception:
    print(f'Pool {pool_name3} not found.')

# Delete partition
try:
    device.delete(path=f'/mgmt/tm/sys/folder/{rest_format(partition_name)}')
    print(f'Folder {partition_name} deleted.')
except Exception:
    print(f'Folder {partition_name} not found.')
