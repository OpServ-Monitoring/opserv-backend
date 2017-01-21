import os
from argparse import ArgumentParser
from unittest import TestCase

from application_settings.logging_settings import LoggingSettings


class TestLoggingSettings(TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

        open("test.log", "w").close()

    def test_add_settings_arguments(self):
        LoggingSettings.add_settings_arguments(self.parser)

        try:
            self.parser.parse_args("-cl".split())
            self.parser.parse_args("--consolelog".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        try:
            self.parser.parse_args("-fl".split())
            self.parser.parse_args("--filelog".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        try:
            self.parser.parse_args("-cl debug".split())
            self.parser.parse_args("--consolelog debug".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        try:
            self.parser.parse_args("-fl test.log".split())
            self.parser.parse_args("--filelog test.log".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

    def tearDown(self):
        # TODO Use more stable approach
        try:
            os.remove("test.log")
        except PermissionError:
            print("Could not delete file: test.log")
