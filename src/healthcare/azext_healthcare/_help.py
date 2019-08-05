# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=line-too-long
from knack.help_files import helps  # pylint: disable=unused-import


helps['healthcareapis'] = """
    type: group
    short-summary: Commands to manage service.
"""

helps['healthcareapis create'] = """
    type: command
    short-summary: create service.
    examples:
      - name: ServicePut
        text: |-
               az healthcareapis create --resource-group "rg1" --name "service1" --kind "fhir" \\
               --location "westus"
"""

helps['healthcareapis update'] = """
    type: command
    short-summary: update service.
    examples:
      - name: ServicePatch
        text: |-
               az healthcareapis update --resource-group "rg1" --name "service1"
"""

helps['healthcareapis delete'] = """
    type: command
    short-summary: delete service.
    examples:
      - name: ServiceDelete
        text: |-
               az healthcareapis delete --resource-group "rg1" --name "service1"
"""

helps['healthcareapis list'] = """
    type: command
    short-summary: list service.
"""

helps['healthcareapis show'] = """
    type: command
    short-summary: show service.
"""
