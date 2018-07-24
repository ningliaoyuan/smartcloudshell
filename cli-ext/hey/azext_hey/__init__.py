# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader

import azext_hey._help  # pylint: disable=unused-import


class HeyCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        hey_custom = CliCommandType(
            operations_tmpl='azext_hey.custom#{}')
        super(HeyCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                custom_command_type=hey_custom)

    def load_command_table(self, _):
        with self.command_group('') as g:
            g.custom_command('hey', 'hey')
        return self.command_table

    def load_arguments(self, _):
        # pylint: disable=line-too-long
        with self.argument_context('hey') as c:
            c.positional('keywords', nargs='+', help='space separated keywords')

COMMAND_LOADER_CLS = HeyCommandsLoader
