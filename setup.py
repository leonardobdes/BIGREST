import setuptools
from bigrest.version import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bigrest",
    version=__version__,
    author="Leonardo Souza",
    description="A Python SDK for F5 iControl REST API",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/leonardobdes/BIGREST",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
