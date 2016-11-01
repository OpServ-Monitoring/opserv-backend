import os
from argparse import ArgumentParser, Namespace
from unittest import TestCase

from app.application_settings.configuration_settings import ConfigurationSettings


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

        with open("test.conf", "w") as file:
            file.write("{}")

        with open("test.conf", "r") as file:
            args.conf_file = file

            try:
                ConfigurationSettings.validate_settings_arguments(self.parser, args)
            except SystemExit:
                self.fail("validate_settings_arguments() raised SystemExit unexpectedly!")

        with open("test.conf", "w") as file:
            file.write("[]")

        with open("test.conf", "r") as file:
            args.conf_file = file

            with self.assertRaises(SystemExit) as cm:
                ConfigurationSettings.validate_settings_arguments(self.parser, args)
            self.assertEqual(cm.exception.code, 2)

        with open("test.conf", "w") as file:
            file.write("2")

        with open("test.conf", "r") as file:
            args.conf_file = file

            with self.assertRaises(SystemExit) as cm:
                ConfigurationSettings.validate_settings_arguments(self.parser, args)
            self.assertEqual(cm.exception.code, 2)

        with open("test.conf", "w") as file:
            file.write(''"A test string"'')

        with open("test.conf", "r") as file:
            args.conf_file = file

            with self.assertRaises(SystemExit) as cm:
                ConfigurationSettings.validate_settings_arguments(self.parser, args)
            self.assertEqual(cm.exception.code, 2)

        with open("test.conf", "w") as file:
            file.write("{2}")

        with open("test.conf", "r") as file:
            args.conf_file = file

            with self.assertRaises(SystemExit) as cm:
                ConfigurationSettings.validate_settings_arguments(self.parser, args)
            self.assertEqual(cm.exception.code, 2)

        with open("test.conf", "w") as file:
            file.write("")

        with open("test.conf", "r") as file:
            args.conf_file = file

            with self.assertRaises(SystemExit) as cm:
                ConfigurationSettings.validate_settings_arguments(self.parser, args)
            self.assertEqual(cm.exception.code, 2)

    def tearDown(self):
        os.remove("test.conf")
