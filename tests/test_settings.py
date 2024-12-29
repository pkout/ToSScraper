import sys
import unittest
from enum import Enum

sys.path.append('src')

from settings import ConfigurationFileNotFound
from settings import settings, Settings

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
        self.assertEqual(settings['candleWidthPx'], 10)