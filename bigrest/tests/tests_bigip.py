"""
BIGREST SDK tests
Perform test on a BIG-IP device
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

# Create a device object with basic authentication
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

# Create folder
data = {}
data['name'] = 'bigrest'
data['partition'] = '/'
partition = device.create(path='/mgmt/tm/sys/folder', data=data)
if partition.properties['fullPath'] != partition_name:
    raise Exception(partition.properties['fullPath'])
else:
    print(f"Partition {partition_name} created.")

# Create pool
data = {}
data['name'] = pool_name
pool = device.create(path='/mgmt/tm/ltm/pool', data=data)
if pool.properties['fullPath'] != pool_name:
    raise Exception(pool.properties['fullPath'])
else:
    print(f"Pool {pool_name} created.")

# Add pool member
data = {}
data ['name'] = member_name
member = device.create(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members', data=data)
if member.properties['fullPath'] != '/bigrest/172.17.0.1:80':
    raise Exception(member.properties['fullPath'])
else:
    print(f"Member {member_name} created.")

# Add virtual server
data = {}
data['name'] = virtual_name
data['destination'] = '10.17.0.1%0:80'
virtual = device.create(path='/mgmt/tm/ltm/virtual', data=data)
if virtual.properties['fullPath'] != virtual_name:
    raise Exception(virtual.properties['fullPath'])
else:
    print(f'Virtual {virtual_name} created.')

# Add pool to virtual server
virtual = device.load(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}')
virtual = virtual[0]
virtual.properties['pool'] = pool_name
virtual_updated = device.save(virtual)
if virtual_updated.properties['pool'] != pool_name:
    raise Exception(virtual_updated.properties['pool_name'])
else:
    print(f"Virtual {virtual_name} modified.")

# Print virtual servers name
virtuals = device.load(path='/mgmt/tm/ltm/virtual')
print('List all virtual servers:')
for virtual in virtuals:
    print(virtual.properties['name'])

# Print node
node = device.load(path=f'/mgmt/tm/ltm/node/{rest_format(node_name)}')
node = node[0]
print('Print node:')
print(node)

# Modify pool description
data = {}
description = "bigrest"
data['description'] = description
pool_updated = device.modify(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}', data=data)
if pool_updated.properties['description'] != description:
    raise Exception(pool_updated.properties['description'])
else:
    print(f"Pool {virtual_name} modified.")

# Test if virtual server exists
if device.exist(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}'):
    print(f'Virtual {virtual_name} exists.')
else:
    raise Exception(f'Error testing if {virtual_name} exists.')
fake_virtual_name = '/Common/fake'
if device.exist(path=f'/mgmt/tm/ltm/virtual/{rest_format(fake_virtual_name)}'):
    raise Exception(f"Error testing if {fake_virtual_name} exists.")
else:
    print(f"Virtual {fake_virtual_name} does not exist.")

# Show virtual server information
virtual = device.show(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}')
virtual = virtual[0]
if virtual.properties['clientside.maxConns']['value'] != 0:
    raise Exception(virtual.properties['clientside.maxConns']['value'])
else:
    print(f"Virtual {virtual_name} maximum number of connections.")

# Test transaction
transaction_start = device.transaction_start()
transaction_id = transaction_start.properties['transId']
print(f"Transaction ID: {transaction_id}.")
data = {}
data['name'] = pool_name2
device.create(path='/mgmt/tm/ltm/pool', data=data)
data = {}
data['name'] = virtual_name2
data['destination'] = '10.17.0.2%0:80'
device.create(path='/mgmt/tm/ltm/virtual', data=data)
device.transaction_finish()
print(f'Transaction {transaction_id} completed.')

# Test transaction with "with"
with device as transaction:
    data = {}
    data['name'] = pool_name3
    device.create(path='/mgmt/tm/ltm/pool', data=data)
    data = {}
    data['name'] = virtual_name3
    data['destination'] = '10.17.0.3%0:80'
    device.create(path='/mgmt/tm/ltm/virtual', data=data)
print('Transaction with "with" completed.')

# Test transaction functions
transaction_start = device.transaction_start()
transaction_id = transaction_start.properties['transId']
print(f"Transaction ID: {transaction_id}.")
data = {}
data['name'] = pool_name2
device.create(path='/mgmt/tm/ltm/pool', data=data)
data = {}
data['name'] = virtual_name2
data['destination'] = '10.17.0.2%0:80'
device.create(path='/mgmt/tm/ltm/virtual', data=data)
try:
    device.transaction_validate()
    raise Exception('Transaction should have failed.')
except Exception:
    print('Transaction validated.')
device.transaction_delete()
print('Transaction deleted.')

# Delete pool member
device.delete(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(member_name)}')
print(f'Member {member_name} deleted.')

# Delete node
device.delete(path=f'/mgmt/tm/ltm/node/{rest_format(node_name)}')
print(f'Node {node_name} deleted.')

# Delete virtual
device.delete(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name)}')
print(f'Virtual {virtual_name} deleted.')

# Delete virtual
device.delete(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name2)}')
print(f'Virtual {virtual_name2} deleted.')

# Delete virtual
device.delete(path=f'/mgmt/tm/ltm/virtual/{rest_format(virtual_name3)}')
print(f'Virtual {virtual_name3} deleted.')

# Delete pool
device.delete(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}')
print(f'Pool {pool_name} deleted.')

# Delete pool
device.delete(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name2)}')
print(f'Pool {pool_name2} deleted.')

# Delete pool
device.delete(path=f'/mgmt/tm/ltm/pool/{rest_format(pool_name3)}')
print(f'Pool {pool_name3} deleted.')

# Delete partition
device.delete(path=f'/mgmt/tm/sys/folder/{rest_format(partition_name)}')
print(f'Partition {partition_name} deleted.')