from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

solution_items = (
    # Solution Template Menu Item
        PluginMenuItem(
        link="plugins:netbox_servicemgmt:solutionrequest_list",
        link_text="Solution Requests",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:solutionrequest_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_servicemgmt:solutionrequest_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:solutiontemplate_list",
        link_text="Solutions",
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
)
service_items = ( 
    # Service Requirement Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:servicetemplate_list",
        link_text="Services",
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
    ),    # Service Requirement Menu Item
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
    # Service Deployment Menu Item
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:servicedeployment_list",
        link_text="Deployments",
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
        link_text="Deployment Components",
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
)
profile_items = (
    PluginMenuItem(
        link="plugins:netbox_servicemgmt:faulttolerance_list",
        link_text="Fault Tolerance Profiles",
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
    groups=(("SOLUTIONS", solution_items),("SERVICES", service_items),("PROFILES", profile_items)),
    icon_class="mdi mdi-server",
)
