"""BIGREST SDK tests file"""

# External Imports
# Import only with 'import package',
# it will make explicity in the code where it came from.
import getpass

# BIGREST Imports
# Import only with 'from x import y', to simplify the code.
from ..bigrest import BIGREST

# Get username, password, and ip
username = getpass.getuser()
password = getpass.getpass()
print('Device IP or name:')
ip = input()

# Create a device object
device = BIGREST(device=ip, username=username, password=password)

virtual = device.load('/mgmt/tm/ltm/virtual/vs_asm')
print(virtual[0].properties['name'])