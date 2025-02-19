from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

solution_items = (
    # Solution Template Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:solution_list",
        link_text="Solutions",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:solution_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:solution_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:deployment_list",
        link_text="Deployments",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:deployment_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:deployment_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Component Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:component_list",
        link_text="Deployment Components",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:component_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:component_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
)
profile_items = (
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:faulttolerence_list",
        link_text="Fault Tolerence Profiles",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:faulttolerence_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:faulttolerence_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # SLO Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:slo_list",
        link_text="SLO Profiles",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:slo_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:slo_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
)

# Define the top-level menu with icon
menu = PluginMenu(
    label="Service Management",
    groups=(("SOLUTIONS", solution_items),("PROFILES", profile_items)),
    icon_class="mdi mdi-server",
)
