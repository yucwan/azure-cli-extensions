# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def create_scsx(cmd, resource_group_name, scsx_name, location=None, tags=None):
    raise CLIError('TODO: Implement `scsx create`')


def list_scsx(cmd, resource_group_name=None):
    raise CLIError('TODO: Implement `scsx list`')


def update_scsx(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param('tags', tags)
    return instance