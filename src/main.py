import json
from pathlib import Path

import pyautogui

from candle_scraper import CandleScraper
import utils

class TickerSymbolScraper:

    def __init__(self, candle_scraper):
        self._candle_scraper = candle_scraper

    def scrape_candles_in_date_range(self, symbol, chart_pages_count_to_read=None):
        candles_values = self._candle_scraper.scrape()

        return candles_values

    def save(self, _dict, path):
        if _dict is None:
            raise ValueError('The _dict argument cannot be None!')

        utils.ensure_dir_exists(path.parent.absolute())

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(_dict, f, indent=4)

def _save_file_path(symbol):
    dir_path = Path(__file__).parent / Path('data')
    return dir_path / Path(f'{symbol}.json')

if __name__ == '__main__':
    symbol = 'UVIX'

    candle_scraper = CandleScraper(
        gui_controller=pyautogui,
        ticker_symbol=symbol
    )

    scraper = TickerSymbolScraper(candle_scraper)
    candle_values = scraper.scrape_candles_in_date_range(symbol)
    scraper.save(candle_values, _save_file_path(symbol))
