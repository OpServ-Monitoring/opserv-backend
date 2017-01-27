from unittest import TestCase

from application_settings import _settings_base as application_settings
from application_settings._settings_base import SettingsBase


class TestSettingsBase(TestCase):
    def setUp(self):
        application_settings.settings = {
            "test_0": "hello",
            "test_1": 0
        }

    def test_get_setting(self):
        self.assertEqual(
            SettingsBase.get_setting("test_0"),
            "hello"
        )

        self.assertEqual(
            SettingsBase.get_setting("test_1"),
            0
        )

        self.assertIsNone(
            SettingsBase.get_setting("test_2")
        )

    def tearDown(self):
        application_settings.settings = None
