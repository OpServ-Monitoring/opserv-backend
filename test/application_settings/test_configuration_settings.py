import json
import os
from argparse import ArgumentParser, Namespace

from application_settings.configuration_settings import ConfigurationSettings
from unittest import TestCase


class TestConfigurationSettings(TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

        open("test.conf", "w").close()

    def test_add_settings_arguments(self):
        ConfigurationSettings.add_settings_arguments(self.parser)

        try:
            self.parser.parse_args("-cf test.conf".split())
            self.parser.parse_args("--conf-file test.conf".split())
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

    def test_validate_settings_arguments(self):
        args = Namespace()
        args.conf_file = "test.conf"

        file = open("test.conf", "w")
        file.write("{}")
        file.close()
        try:
            ConfigurationSettings.validate_settings_arguments(self.parser, args)
        except SystemExit:
            self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        file = open("test.conf", "w")
        file.write("{2}")
        file.close()
        with self.assertRaises(SystemExit) as cm:
            ConfigurationSettings.validate_settings_arguments(self.parser, args)
        self.assertEqual(cm.exception.code, 2)

    def tearDown(self):
        os.remove("test.conf")
