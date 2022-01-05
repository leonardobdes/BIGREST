"""File with version and history information."""

__version__ = '1.4.0'

"""
History Information:
1.0.0
    First Version
1.0.1
    Removed tests folder from pip
1.0.2
    Fixed documentation
1.0.3
    Fixed documentation
1.0.4
    Fixed issue #4
1.1.0
    Corrected version number.
    Previous should have been 1.1.0 as it changes function behaviour.
1.2.0
    Moved debug functionality to a separated file.
    Debug output now includes curl command.
1.3.0
    Fixed issue #7
1.3.1
    Fix for issue #7 caused problems to BIG-IQ.
    Checking "collection" for BIG-IP and now "com.f5.rest.common" for BIG-IQ.
1.3.2
    Fixed issue #8
1.3.3
    Add 202 respose to create method.
    Updated documentation about upload and download methods
    Removed unnecessary f-strings
1.3.4
    Fixed documentation typos in bigiq_load.rst and utils.rst files.
1.4.0
    Fixed issue #13
"""
