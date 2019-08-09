# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

def load_command_table(self, _):

    with self.command_group('scs') as g:
        g.custom_command('create', 'scs_create')
        g.custom_command('delete', 'scs_delete')
        g.custom_command('list', 'scs_list')
        g.custom_command('show', 'scs_get')
        g.custom_command('update', 'scs_update')
        g.custom_command('debuggingkey', 'scs_debuggingkey')
        # g.generic_update_command('update', setter_name='update', custom_func_name='update_scs')

    with self.command_group('scs app') as g:
        g.custom_command('create', 'app_create')
        g.custom_command('update', 'app_update')
        g.custom_command('deploy', 'app_deploy')
        g.custom_command('delete', 'app_delete')
        g.custom_command('list', 'app_list')
        g.custom_command('show', 'app_get')
        g.custom_command('start', 'app_start')
        g.custom_command('stop', 'app_stop')
        g.custom_command('restart', 'app_restart')

    with self.command_group('scs app deployment') as g:
        g.custom_command('create', 'deployment_create')
        g.custom_command('set-active', 'deployment_activate')
        g.custom_command('list', 'deployment_list')
        g.custom_command('show', 'deployment_get')
        g.custom_command('delete', 'deployment_delete')

    with self.command_group('scs', is_preview=True):
        pass