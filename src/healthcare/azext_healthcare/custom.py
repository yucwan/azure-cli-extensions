# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
# pylint: disable=too-many-statements
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=unused-argument

import json


# module equivalent: azure_rm_healthcareapisservice
# URL: /subscriptions/{{ subscription_id }}/resourceGroups/{{ resource_group }}/providers/Microsoft.HealthcareApis/services/{{ service_name }}
def create_healthcareapis(cmd, client,
                          resource_group,
                          name,
                          kind,
                          location,
                          access_policies_object_id,
                          tags=None,
                          etag=None,
                          cosmos_db_offer_throughput=None,
                          authentication_authority=None,
                          authentication_audience=None,
                          authentication_smart_proxy_enabled=None,
                          cors_origins=None,
                          cors_headers=None,
                          cors_methods=None,
                          cors_max_age=None,
                          cors_allow_credentials=None):
    return client.create_or_update(resource_group_name=resource_group, resource_name=name)


# module equivalent: azure_rm_healthcareapisservice
# URL: /subscriptions/{{ subscription_id }}/resourceGroups/{{ resource_group }}/providers/Microsoft.HealthcareApis/services/{{ service_name }}
def update_healthcareapis(cmd, client, body,
                          resource_group,
                          name,
                          kind,
                          location,
                          access_policies_object_id,
                          tags=None,
                          etag=None,
                          cosmos_db_offer_throughput=None,
                          authentication_authority=None,
                          authentication_audience=None,
                          authentication_smart_proxy_enabled=None,
                          cors_origins=None,
                          cors_headers=None,
                          cors_methods=None,
                          cors_max_age=None,
                          cors_allow_credentials=None):
    return client.create_or_update(resource_group_name=resource_group, resource_name=name)


# module equivalent: azure_rm_healthcareapisservice
# URL: /subscriptions/{{ subscription_id }}/resourceGroups/{{ resource_group }}/providers/Microsoft.HealthcareApis/services/{{ service_name }}
def list_healthcareapis(cmd, client,
                        resource_group):
    if resource_group is not None:
        return client.list_by_resource_group(resource_group_name=resource_group)
    return client.list()
