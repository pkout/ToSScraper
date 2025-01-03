import json
import tempfile
import unittest
from unittest.mock import Mock
from pathlib import Path

from main import TickerSymbolScraper
from candle_scraper import CandleScraper
from chart_paginator import ChartPaginator

FIXTURES_DIR = Path(__file__).parent / Path('fixtures')

class TestTickerSymbolScraper(unittest.TestCase):

    def setUp(self):
        self.mock_chart_paginator = Mock(spec=ChartPaginator)
        self.mock_candle_scraper = Mock(spec=CandleScraper)

        self.scraper = TickerSymbolScraper(
            self.mock_chart_paginator,
            self.mock_candle_scraper
        )

    def test_instantiates(self):
        self.assertIsInstance(self.scraper, TickerSymbolScraper)

    def test_scrape_returns_expected_value_dict(self):
        expected_dict = {'my': 'data'}
        self.mock_candle_scraper.scrape.return_value = expected_dict

        candles_values = self.scraper.scrape_candles_in_date_range('uvix')

        self.assertDictEqual(candles_values, expected_dict)

    def test_save_raises_if_dict_is_none(self):
        path = Path(tempfile.gettempdir()) / Path('test_save_saves_symbol_values_to_file.json')

        with self.assertRaises(ValueError):
            self.scraper.save(None, path)

    def test_save_saves_symbol_values_to_file(self):
        dict_to_save = {'my': 'data'}
        path = Path(tempfile.gettempdir()) / Path('test_save_saves_symbol_values_to_file.json')

        self.scraper.save(dict_to_save, path)

        with open(path, 'r', encoding='utf-8') as f:
            file_json = json.load(f)

        self.assertDictEqual(file_json, dict_to_save)

if __name__ == '__main__':
    unittest.main()