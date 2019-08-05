# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements

from knack.arguments import CLIArgumentType
from azure.cli.core.commands.parameters import (
    tags_type,
    get_three_state_flag,
    get_enum_type,
    resource_group_name_type,
    get_location_type
)
from azure.cli.core.commands.validators import get_default_location_from_resource_group


def load_arguments(self, _):
    name_arg_type = CLIArgumentType(options_list=('--name', '-n'), metavar='NAME')

    with self.argument_context('healthcare create') as c:
        c.argument('resource_group', resource_group_name_type)
        c.argument('name', id_part=None, help='The name of the service instance.')
        c.argument('kind', arg_type=get_enum_type(['fhir', 'fhir-Stu3', 'fhir-R4']), id_part=None, help='The kind of the service. Valid values are: fhir, fhir-Stu3 and fhir-R4.')
        c.argument('location', arg_type=get_location_type(self.cli_ctx))
        c.argument('tags', tags_type)
        c.argument('etag', id_part=None, help='An etag associated with the resource, used for optimistic concurrency when editing it.')
        c.argument('access_policies', id_part=None, help='The access policies of the service instance.')
        c.argument('cosmos_db_configuration', id_part=None, help='The settings for the Cosmos DB database backing the service.')
        c.argument('authentication_configuration', id_part=None, help='The authentication configuration for the service instance.')
        c.argument('cors_configuration', id_part=None, help='The settings for the CORS configuration of the service instance.')

    with self.argument_context('healthcare update') as c:
        c.argument('resource_group', resource_group_name_type)
        c.argument('name', id_part=None, help='The name of the service instance.')
        c.argument('kind', arg_type=get_enum_type(['fhir', 'fhir-Stu3', 'fhir-R4']), id_part=None, help='The kind of the service. Valid values are: fhir, fhir-Stu3 and fhir-R4.')
        c.argument('location', arg_type=get_location_type(self.cli_ctx))
        c.argument('tags', tags_type)
        c.argument('etag', id_part=None, help='An etag associated with the resource, used for optimistic concurrency when editing it.')
        c.argument('access_policies', id_part=None, help='The access policies of the service instance.')
        c.argument('cosmos_db_configuration', id_part=None, help='The settings for the Cosmos DB database backing the service.')
        c.argument('authentication_configuration', id_part=None, help='The authentication configuration for the service instance.')
        c.argument('cors_configuration', id_part=None, help='The settings for the CORS configuration of the service instance.')

    with self.argument_context('healthcare delete') as c:
        c.argument('resource_group', resource_group_name_type)
        c.argument('name', id_part=None, help='The name of the service instance.')

    with self.argument_context('healthcare list') as c:
        c.argument('resource_group', resource_group_name_type)

    with self.argument_context('healthcare show') as c:
        c.argument('resource_group', resource_group_name_type)
        c.argument('name', id_part=None, help='The name of the service instance.')
