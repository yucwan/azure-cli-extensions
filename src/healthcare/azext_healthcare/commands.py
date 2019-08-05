# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
from azext_healthcare._client_factory import cf_healthcare


def load_command_table(self, _):

    # TODO: Add command type here
    # healthcare_sdk = CliCommandType(
    #    operations_tmpl='<PATH>.operations#None.{}',
    #    client_factory=cf_healthcare)


    with self.command_group('healthcare') as g:
        g.custom_command('create', 'create_healthcare')
        # g.command('delete', 'delete')
        g.custom_command('list', 'list_healthcare')
        # g.show_command('show', 'get')
        # g.generic_update_command('update', setter_name='update', custom_func_name='update_healthcare')


    with self.command_group('healthcare', is_preview=True):
        pass

