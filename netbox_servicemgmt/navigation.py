from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

items = (
    # Solution Template Menu Item
    PluginMenuItem(
        link="plugins:netbox_service_plugin:solutiontemplate_list",
        link_text="Solution Templates",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_plugin:solutiontemplate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_plugin:solutiontemplate_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Template Menu Item
    PluginMenuItem(
        link="plugins:netbox_service_plugin:servicetemplate_list",
        link_text="Service Templates",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_plugin:servicetemplate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_plugin:servicetemplate_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Requirement Menu Item
    PluginMenuItem(
        link="plugins:netbox_service_plugin:servicerequirement_list",
        link_text="Service Requirements",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_plugin:servicerequirement_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_plugin:servicerequirement_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Solution Deployment Menu Item
    PluginMenuItem(
        link="plugins:netbox_service_plugin:solutiondeployment_list",
        link_text="Solution Deployments",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_plugin:solutiondeployment_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_plugin:solutiondeployment_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Deployment Menu Item
    PluginMenuItem(
        link="plugins:netbox_service_plugin:servicedeployment_list",
        link_text="Service Deployments",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_plugin:servicedeployment_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_plugin:servicedeployment_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Component Menu Item
    PluginMenuItem(
        link="plugins:netbox_service_plugin:servicecomponent_list",
        link_text="Service Components",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_plugin:servicecomponent_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_plugin:servicecomponent_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # HA Model Menu Item
    PluginMenuItem(
        link="plugins:netbox_service_plugin:hamodel_list",
        link_text="HA Models",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_plugin:hamodel_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_plugin:hamodel_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # SLO Menu Item
    PluginMenuItem(
        link="plugins:netbox_service_plugin:slo_list",
        link_text="SLOs",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_plugin:slo_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_plugin:slo_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
)

# Define the top-level menu with icon
menu = PluginMenu(
    label="Service Management",
    groups=(("SERVICE MANAGEMENT", items),),
    icon_class="mdi mdi-server",
)
