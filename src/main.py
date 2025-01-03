import json
from pathlib import Path

import pyautogui

from candle_scraper import CandleScraper
from chart_paginator import ChartPaginator
import utils

class TickerSymbolScraper:

    def __init__(self, chart_paginator, candle_scraper):
        self._chart_paginator = chart_paginator
        self._candle_scraper = candle_scraper

    def scrape_candles_in_date_range(self, symbol, chart_pages_count_to_read=None):
        self._chart_paginator.next_page()
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
    _symbol = 'UVIX'

    candle_scraper = CandleScraper(pyautogui, _symbol)
    chart_paginator = ChartPaginator(pyautogui)
    scraper = TickerSymbolScraper(chart_paginator, candle_scraper)
    candle_values = scraper.scrape_candles_in_date_range(_symbol)
    scraper.save(candle_values, _save_file_path(_symbol))
