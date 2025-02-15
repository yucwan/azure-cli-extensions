# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.profiles import ResourceType
from azure.cli.core.profiles import CustomResourceType

CUSTOM_MGMT_AKS_PREVIEW = CustomResourceType('azext_aks_preview.vendored_sdks.azure_mgmt_preview_aks',
                                             'ContainerServiceClient')
CUSTOM_MGMT_AKS = CustomResourceType('azext_aks_preview.vendored_sdks.azure_mgmt_aks',
                                     'ContainerServiceClient')


def cf_compute_service(cli_ctx, *_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_COMPUTE)


def cf_container_services(cli_ctx, *_):
    return get_container_service_client(cli_ctx).container_services


def get_container_service_client(cli_ctx, **_):
    return get_mgmt_service_client(cli_ctx, CUSTOM_MGMT_AKS_PREVIEW)


def cf_managed_clusters(cli_ctx, *_):
    return get_mgmt_service_client(cli_ctx, CUSTOM_MGMT_AKS_PREVIEW).managed_clusters


def cf_agent_pools(cli_ctx, *_):
    return get_mgmt_service_client(cli_ctx, CUSTOM_MGMT_AKS_PREVIEW).agent_pools


def cf_resource_groups(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id).resource_groups


def cf_resources(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id).resources


def get_auth_management_client(cli_ctx, scope=None, **_):
    import re

    subscription_id = None
    if scope:
        matched = re.match('/subscriptions/(?P<subscription>[^/]*)/', scope)
        if matched:
            subscription_id = matched.groupdict()['subscription']
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_AUTHORIZATION, subscription_id=subscription_id)


def get_graph_rbac_management_client(cli_ctx, **_):
    from azure.cli.core.commands.client_factory import configure_common_settings
    from azure.cli.core._profile import Profile
    from azure.graphrbac import GraphRbacManagementClient

    profile = Profile(cli_ctx=cli_ctx)
    cred, _, tenant_id = profile.get_login_credentials(
        resource=cli_ctx.cloud.endpoints.active_directory_graph_resource_id)
    client = GraphRbacManagementClient(
        cred, tenant_id,
        base_url=cli_ctx.cloud.endpoints.active_directory_graph_resource_id)
    configure_common_settings(cli_ctx, client)
    return client
