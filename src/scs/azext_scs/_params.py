# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType


def load_arguments(self, _):

    from azure.cli.core.commands.parameters import tags_type
    from azure.cli.core.commands.validators import get_default_location_from_resource_group

    scs_name_type = CLIArgumentType(options_list='--scs-name-name', help='Name of the Scs.', id_part='name')

    with self.argument_context('scs') as c:
        c.argument('tags', tags_type)
        c.argument('location', validator=get_default_location_from_resource_group)
        c.argument('scs_name', scs_name_type, options_list=['--name', '-n'])

    with self.argument_context('scs app') as c:
        c.argument('scs_name', scs_name_type, id_part=None)
