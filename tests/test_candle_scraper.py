import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import pyautogui
from PIL import Image

from .misc import patch_settings_file
from candle_scraper import CandleScraper

FIXTURES_DIR = Path(__file__).parent / Path('fixtures')

class TestCandleScraper(unittest.TestCase):

    def setUp(self):
        self._mock_gui_controller()
        self.scraper = CandleScraper(self.mock_gui_controller, 'uvix')

    def _mock_gui_controller(self):
        self.mock_gui_controller = Mock(spec=pyautogui)
        self.mock_gui_controller.size.return_value = 300, 500

    def tearDown(self):
        if hasattr(self, 'ohlcv_screenshot'):
            self.ohlcv_screenshot.close()

        if hasattr(self, 'rsi_screenshot'):
            self.rsi_screenshot.close()

        if hasattr(self, 'ohlcv_screenshot2'):
            self.ohlcv_screenshot2.close()

        if hasattr(self, 'rsi_screenshot2'):
            self.rsi_screenshot2.close()

    def test_instantiates(self):
        self.assertIsInstance(self.scraper, CandleScraper)

    def test_scrape_moves_mouse_in_front_of_first_candle(self):
        self._prepare_single_candle()

        self.scraper.scrape()

        self.mock_gui_controller.moveTo.assert_called_once_with(290, 250.0, 0)

    @patch('candle_scraper.settings', patch_settings_file('cursorStepsCount', 1))
    def test_scrape_moves_mouse_to_next_candle(self):
        self._prepare_single_candle()

        self.scraper.scrape()

        self.mock_gui_controller.moveRel.assert_called_once_with(1, 0, duration=0)

    @patch('candle_scraper.settings', patch_settings_file('cursorStepsCount', 1))
    def test_scrape_returns_candle_values(self):
        self._prepare_single_candle()

        candles_values = self.scraper.scrape()

        self.assertDictEqual(
            candles_values['ohlcv'][0],
            {
                't': 1655378100000, 'o': 1071.0, 'h': 1084.5,
                'l': 1069.0, 'c': 1078.0, 'v': 2426
            }
        )

        self.assertDictEqual(candles_values['rsi'][0], {'rsi': 47.2149})
        self.assertEqual(len(candles_values['ohlcv']), 1)
        self.assertEqual(len(candles_values['rsi']), 1)

    @patch('candle_scraper.settings', patch_settings_file('cursorStepsCount', 2))
    def test_scrape_returns_single_candle_values_if_candle_is_read_twice(self):
        # The cursor advances by steps smaller than the width of a candle,
        # so a candle can be read more than once.
        self._prepare_two_identical_candles()

        candles_values = self.scraper.scrape()

        self.assertEqual(len(candles_values['ohlcv']), 1)
        self.assertEqual(len(candles_values['rsi']), 1)

    @patch('candle_scraper.settings', patch_settings_file('cursorStepsCount', 2))
    def test_scrape_returns_accumulated_candle_values_after_last_candle_read(self):
        # Read 2 candles, but the first candle was the last one,
        # so when reading the second one, it should break out of
        # the reading loop and return the accumulated candle values.
        self._prepare_two_unique_candles()

        candles_values = self.scraper.scrape()

        first_candle_ohlcv = candles_values['ohlcv'][0]
        first_candle_rsi = candles_values['rsi'][0]

        # Check that only the first first candle values were returned.
        self.assertEqual(len(candles_values['ohlcv']), 1)
        self.assertEqual(len(candles_values['rsi']), 1)

        self.assertDictEqual(
            first_candle_ohlcv,
            {
                't': 1655378100000, 'o': 1071.0, 'h': 1084.5,
                'l': 1069.0, 'c': 1078.0, 'v': 2426
            }
        )

        self.assertDictEqual(first_candle_rsi, {'rsi': 47.2149})

    @patch('candle_scraper.settings', patch_settings_file('cursorStepsCount', 1))
    def test_scrape_returns_minus_one_rsi_value_if_screenshot_not_readable(self):
        self._prepare_single_corrupt_rsi_candle()

        candles_values = self.scraper.scrape()

        self.assertEqual(candles_values['rsi'][0]['rsi'], -1)

    @patch('candle_scraper.settings', patch_settings_file('cursorStepsCount', 1))
    def test_scrape_saves_failing_input_screenshot_if_failed_parsing_ohlcv(self):
        self._prepare_single_corrupt_ohlcv_candle()
        save_file_path = Path(__file__).parent.parent / \
                         Path('ohlcv-1655378100000.png')

        save_file_path.unlink(missing_ok=True)

        candle_values = self.scraper.scrape()

        self.assertDictEqual(
            candle_values['ohlcv'][0],
            {'t': 1655378100000, 'c': -1, 'h': -1, 'l': -1, 'o': -1, 'v': -1}
        )

        self.assertTrue(save_file_path.exists())
        save_file_path.unlink()

    def _prepare_two_identical_candles(self):
        self.ohlcv_screenshot = Image.open(FIXTURES_DIR / Path('ohlcv.jpg'))
        self.rsi_screenshot = Image.open(FIXTURES_DIR / Path('rsi.jpg'))

        self.mock_gui_controller.screenshot.side_effect = [self.ohlcv_screenshot,
                                                           self.rsi_screenshot] * 2

    def _prepare_single_candle(self):
        self.ohlcv_screenshot = Image.open(FIXTURES_DIR / Path('ohlcv.jpg'))
        self.rsi_screenshot = Image.open(FIXTURES_DIR / Path('rsi.jpg'))

        self.mock_gui_controller.screenshot.side_effect = [self.ohlcv_screenshot,
                                                           self.rsi_screenshot]

    def _prepare_two_unique_candles(self):
        self.ohlcv_screenshot = Image.open(FIXTURES_DIR / Path('ohlcv.jpg'))
        self.ohlcv_screenshot2 = Image.open(FIXTURES_DIR / Path('ohlcv-stop.jpg'))
        self.rsi_screenshot = Image.open(FIXTURES_DIR / Path('rsi.jpg'))
        self.rsi_screenshot2 = Image.open(FIXTURES_DIR / Path('rsi.jpg'))

        self.mock_gui_controller.screenshot.side_effect = [self.ohlcv_screenshot,
                                                           self.rsi_screenshot,
                                                           self.ohlcv_screenshot2,
                                                           self.rsi_screenshot2]

    def _prepare_single_corrupt_ohlcv_candle(self):
        self.ohlcv_screenshot = Image.open(FIXTURES_DIR / Path('ohlcv-corrupt.jpg'))
        self.rsi_screenshot = Image.open(FIXTURES_DIR / Path('rsi.jpg'))

        self.mock_gui_controller.screenshot.side_effect = [self.ohlcv_screenshot,
                                                           self.rsi_screenshot]

    def _prepare_single_corrupt_rsi_candle(self):
        self.ohlcv_screenshot = Image.open(FIXTURES_DIR / Path('ohlcv.jpg'))
        self.rsi_screenshot = Image.open(FIXTURES_DIR / Path('rsi-corrupt.jpg'))

        self.mock_gui_controller.screenshot.side_effect = [self.ohlcv_screenshot,
                                                           self.rsi_screenshot]