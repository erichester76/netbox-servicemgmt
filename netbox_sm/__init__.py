"""Top-level package for Netbox Service Management Plugin."""

__author__ = "Eric Hester"
__email__ = "hester1@clemson.edu"
__version__ = "0.2.0"

from netbox.plugins import PluginConfig

class smConfig(PluginConfig):
    name = "netbox_sm"
    verbose_name = "Netbox Service Management Plugin"
    description = "Netbox Plugin for Service Management"
    version = "0.2.0"
    base_url = "netboxservicemgmt"

config = smConfig
