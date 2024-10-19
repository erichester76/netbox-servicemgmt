from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

items = (
    # Solution Template Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:solutiontemplate_list",
        link_text="Solution Templates",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:solutiontemplate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:solutiontemplate_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Template Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:servicetemplate_list",
        link_text="Service Templates",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:servicetemplate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:servicetemplate_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Requirement Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:servicerequirement_list",
        link_text="Service Requirements",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:servicerequirement_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:servicerequirement_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Solution Deployment Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:solutiondeployment_list",
        link_text="Solution Deployments",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:solutiondeployment_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:solutiondeployment_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Deployment Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:servicedeployment_list",
        link_text="Service Deployments",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:servicedeployment_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:servicedeployment_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Service Component Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:servicecomponent_list",
        link_text="Service Components",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:servicecomponent_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:servicecomponent_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # Fault Tolerence Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:faulttolerance_list",
        link_text="Fault Tolerance",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:faulttolerance_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:faulttolerance_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    # SLO Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:slo_list",
        link_text="SLOs",
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
    groups=(("SERVICE MANAGEMENT", items),),
    icon_class="mdi mdi-server",
)
