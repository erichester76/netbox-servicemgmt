from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

solution_items = (
    # Solution Template Menu Item
    PluginMenuItem(
        link="plugins:netbox_sm:solution_list",
        link_text="Solutions",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_sm:solution_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_sm:solution_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    PluginMenuItem(
        link="plugins:netbox_sm:deployment_list",
        link_text="Deployments",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_sm:deployment_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_sm:deployment_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Component Menu Item
    PluginMenuItem(
        link="plugins:netbox_sm:component_list",
        link_text="Deployment Components",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_sm:component_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_sm:component_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
)
profile_items = (
    PluginMenuItem(
        link="plugins:netbox_sm:faulttolerence_list",
        link_text="Fault Tolerence Profiles",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_sm:faulttolerence_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_sm:faulttolerence_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # SLO Menu Item
    PluginMenuItem(
        link="plugins:netbox_sm:slo_list",
        link_text="SLO Profiles",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_sm:slo_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_sm:slo_bulk_import",
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
