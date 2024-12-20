"""Top-level package for Netbox Service Management Plugin."""

__author__ = "Eric Hester"
__email__ = "hester1@clemson.edu"
__version__ = "0.1.5"

from netbox.plugins import PluginConfig

class servicemgmtConfig(PluginConfig):
    name = "netbox_servicemgmt"
    verbose_name = "Netbox Service Management Plugin"
    description = "Netbox Plugin for Service Management"
    version = "0.1.5"
    base_url = "netboxservicemgmt"

config = servicemgmtConfig
