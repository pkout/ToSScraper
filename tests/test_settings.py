import unittest
from enum import Enum

from settings import ConfigurationFileNotFound
from settings import profiled_settings, settings, Settings

class TestSettings(unittest.TestCase):

    def setUp(self):
        self.settings = Settings()

    def test_instantiates(self):
        self.assertIsInstance(self.settings, Settings)

    def test_constructor_raises_if_settings_yaml_file_not_found(self):
        class StubEnvironment(Enum):
            nonsense = 'nonsense'

        with self.assertRaises(ConfigurationFileNotFound):
            Settings(StubEnvironment.nonsense)

    def test_as_dict_returns_settings_dict(self):
        self.assertEqual(settings['cursorStepsCount'], 1)

    def test_as_current_profile_dict_returns_current_profile_dict(self):
        self.assertEqual(profiled_settings['candleWidthPx'], 10)