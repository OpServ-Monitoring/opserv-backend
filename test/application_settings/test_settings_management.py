from argparse import ArgumentParser
from unittest import TestCase

from application_settings import settings_management


class TestSettingsManagement(TestCase):
    def test_configure_runtime_arg_parser(self):
        self.assertIsInstance(
            settings_management.configure_runtime_arg_parser(),
            ArgumentParser
        )
