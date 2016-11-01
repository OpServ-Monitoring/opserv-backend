import os
from argparse import ArgumentParser, Namespace
from unittest import TestCase

from app.application_settings.logging_settings import LoggingSettings


class TestLoggingSettings(TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

        open("test.log", "w").close()

    def test_add_settings_arguments(self):
        LoggingSettings.add_settings_arguments(self.parser)

        try:
            self.parser.parse_args("-logtc".split())
            self.parser.parse_args("--log-to-console".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        try:
            self.parser.parse_args("-logtf".split())
            self.parser.parse_args("--log-to-file".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        try:
            self.parser.parse_args("-logl debug".split())
            self.parser.parse_args("--log-level debug".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        try:
            self.parser.parse_args("-logf test.log".split())
            self.parser.parse_args("--logging-file test.log".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

    def test_validate_settings_arguments(self):
        args = Namespace()

        args.log_to_file = None
        args.logging_file = None
        try:
            LoggingSettings.validate_settings_arguments(self.parser, args)
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        args.log_to_file = True
        with self.assertRaises(SystemExit) as cm:
            LoggingSettings.validate_settings_arguments(self.parser, args)
        self.assertEqual(cm.exception.code, 2)

        with open("test.log", "r") as file:
            args.logging_file = file
            try:
                LoggingSettings.validate_settings_arguments(self.parser, args)
            except SystemExit:
                self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

            args.log_to_file = None
            try:
                LoggingSettings.validate_settings_arguments(self.parser, args)
            except SystemExit:
                self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

    def tearDown(self):
        os.remove('test.log')
