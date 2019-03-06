"""Defines the application configuration for the source application"""
from __future__ import unicode_literals

from django.apps import AppConfig


class SourceConfig(AppConfig):
    """Configuration for the source app
    """
    name = 'source'
    label = 'source'
    verbose_name = 'Source'

    def ready(self):
        """
        Override this method in subclasses to run code when Django starts.
        """
        # TODO 1181: Remove usage when remove triggers in v6
        from job.configuration.data.data_file import DATA_FILE_PARSE_SAVER
        from source.configuration.source_data_file import SourceDataFileParseSaver
        # from source.triggers.parse_trigger_handler import ParseTriggerHandler
        # from trigger.handler import register_trigger_rule_handler

        # Register source file parse saver
        # DATA_FILE_PARSE_SAVER['DATA_FILE_PARSE_SAVER'] = SourceDataFileParseSaver()

        # Register parse trigger rule handler
        # register_trigger_rule_handler(ParseTriggerHandler())

        # Register source message types
        from messaging.messages.factory import add_message_type
        from source.messages.purge_source_file import PurgeSourceFile

        add_message_type(PurgeSourceFile)
