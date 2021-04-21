"""
Creates a file with API path list.
"""

# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import getpass

# Internal imports
# Import only with "from x import y", to simplify the code.
from ..bigrest.bigip import BIGIP

# Get username, password, and ip
print("Username: ", end="")
username = input()
password = getpass.getpass()
print("Device IP or name: ", end="")
ip = input()
print("Path: ", end="")
path = input()
print("Filename: ", end="")
filename = input()

# Create a device object with basic authentication
device = BIGIP(ip, username, password)

# Create file
links = device.load(path)
with open(filename, "w") as file_:
    for link in links:
        link_text = link.properties["link"]
        path_to_print = link_text.replace(f"https://localhost{path}", "")
        file_.writelines(f"{path_to_print}\n")

# Sort file content
file_ = open(filename, "r")
lines = file_.readlines()
lines.sort()
file_.close()
file_ = open(filename, "w")
for line in lines:
    file_.write(line)
file_.close()
