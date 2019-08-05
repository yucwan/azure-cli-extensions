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


# module equivalent: azure_rm_healthcareservice
# URL: /subscriptions/{{ subscription_id }}/resourceGroups/{{ resource_group }}/providers/Microsoft.healthcare/services/{{ service_name }}
def create_healthcare(cmd, client,
                          resource_group,
                          name,
                          kind,
                          location,
                          access_policies,
                          tags=None,
                          etag=None,
                          cosmos_db_configuration=None,
                          authentication_configuration=None,
                          cors_configuration=None):

    service_description={}
    service_description['location'] = location
    service_description['kind'] = kind
    service_description['properties'] = {}
    service_description['properties']['access_policies'] = '[{"objectId": "c487e7d1-3210-41a3-8ccc-e9372b78da47"},{"objectId": "5b307da8-43d4-492b-8b66-b0294ade872f"}]'
    service_description['properties']['cors_configuration'] = {}
    service_description['properties']['cors_configuration']['origins'] = ['*']
    service_description['properties']['cors_configuration']['headers'] = ['*']
    service_description['properties']['cors_configuration']['methods'] = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
    service_description['properties']['cors_configuration']['max_age'] = 1440
    service_description['properties']['cors_configuration']['allow_credentials'] = False
    service_description['properties']['cosmos_db_configuration'] = {
          "offerThroughput": 1000
        }
    service_description['authentication_configuration'] = {
          "authority": "https://login.microsoftonline.com/common",
          "audience": "https://azurehealthcareapis.com",
          "smart_proxy_enabled": False
        }

    return client.create_or_update(resource_group_name=resource_group, resource_name=name, service_description=service_description)


# module equivalent: azure_rm_healthcareservice
# URL: /subscriptions/{{ subscription_id }}/resourceGroups/{{ resource_group }}/providers/Microsoft.healthcare/services/{{ service_name }}
def update_healthcare(cmd, client, body,
                          resource_group,
                          name,
                          kind,
                          location,
                          access_policies,
                          tags=None,
                          etag=None,
                          cosmos_db_configuration=None,
                          authentication_configuration=None,
                          cors_configuration=None):
    return client.create_or_update(resource_group_name=resource_group, resource_name=name)


# module equivalent: azure_rm_healthcareservice
# URL: /subscriptions/{{ subscription_id }}/resourceGroups/{{ resource_group }}/providers/Microsoft.healthcare/services/{{ service_name }}
def list_healthcare(cmd, client,
                        resource_group):
    if resource_group is not None:
        return client.list_by_resource_group(resource_group_name=resource_group)
    return client.list()
