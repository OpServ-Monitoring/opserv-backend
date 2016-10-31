from argparse import ArgumentParser, Namespace
from unittest import TestCase

from application_settings.server_settings import ServerSettings


class TestServerSettings(TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    def test_add_settings_arguments(self):
        ServerSettings.add_settings_arguments(self.parser)

        try:
            self.parser.parse_args("-p 31337".split())
            self.parser.parse_args("--port 31337".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

    def test_validate_settings_arguments(self):
        args = Namespace()

        ### PORT ARGUMENT ###
        args.port = -1
        with self.assertRaises(SystemExit) as cm:
            ServerSettings.validate_settings_arguments(self.parser, args)
        self.assertEqual(cm.exception.code, 2)

        args.port = 0
        try:
            ServerSettings.validate_settings_arguments(self.parser, args)
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        args.port = 65535
        try:
            ServerSettings.validate_settings_arguments(self.parser, args)
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        args.port = 65536
        with self.assertRaises(SystemExit) as cm:
            ServerSettings.validate_settings_arguments(self.parser, args)
        self.assertEqual(cm.exception.code, 2)

        args.port = None
        try:
            ServerSettings.validate_settings_arguments(self.parser, args)
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")
