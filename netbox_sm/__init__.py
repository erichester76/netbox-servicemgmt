"""Top-level package for Netbox Service Management Plugin."""

from netbox.plugins import PluginConfig

class smConfig(PluginConfig):
    name = "netbox_sm"
    author = "Eric Hester"
    author_email = "hester1@clemson.edu"
    verbose_name = "Netbox Service Management Plugin"
    description = "Netbox Plugin for Service Management"
    version = "0.2.1"
    base_url = "netboxservicemgmt"

config = smConfig
