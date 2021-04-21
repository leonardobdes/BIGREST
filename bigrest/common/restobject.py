# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
import json


class RESTObject():
    """
    Represents a object created from a response of the iControl REST API.

    Parameters:
        properties: Represents the properties of the object.
    """

    def __init__(self, properties: dict) -> RESTObject:
        self.properties = properties

    def asdict(self) -> dict:
        """Converts the object to a dictionary."""

        # iControl REST API only accepts enabled=True or disabled=True
        if "enabled" in self.properties:
            if self.properties["enabled"] is True:
                self.properties.pop("enabled")
                self.properties["disabled"] = True
        if "disabled" in self.properties:
            if self.properties["disabled"] is True:
                self.properties.pop("disabled")
                self.properties["enabled"] = True

        return self.properties

    def __str__(self) -> str:
        """Converts the object to a string."""

        return json.dumps(self.properties, indent=4)
