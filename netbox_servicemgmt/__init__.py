"""Top-level package for Netbox Service Management Plugin."""

__author__ = "Eric Hester"
__email__ = "hester1@clemson.edu"
__version__ = "0.0.3"


from netbox.plugins import PluginConfig


class servicemgmtConfig(PluginConfig):
    name = "netbox_servicemgmt"
    verbose_name = "Netbox Service Management Plugin"
    description = "Netbox Plugin for Service Management"
    version = "0.0.3"
    base_url = "netbox_servicemgmt"


config = servicemgmtConfig
