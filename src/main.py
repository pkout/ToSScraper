import json
from pathlib import Path

import pyautogui

import utils
from candle_scraper import CandleScraper
from chart_paginator import ChartPaginator
from settings import settings


class TickerSymbolScraper:

    def __init__(self, chart_paginator, candle_scraper):
        self._chart_paginator = chart_paginator
        self._candle_scraper = candle_scraper

    def scrape_candles_in_date_range(self, symbol, chart_pages_count_to_read=None):
        for page_idx in range(settings['numOfPagesToScrape']):
            self._chart_paginator.next_page()
            candles_values = self._candle_scraper.scrape()
            self.save(candles_values, _save_file_path(symbol, page_idx + 1))

    def save(self, _dict, path):
        if _dict is None:
            raise ValueError('The _dict argument cannot be None!')

        utils.ensure_dir_exists(path.parent.absolute())

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(_dict, f, indent=4)

def _save_file_path(symbol, index):
    dir_path = Path(__file__).parent.parent / Path('data')
    return dir_path / Path(f'{symbol}-{index}.json')

if __name__ == '__main__':
    _symbol = 'UVIX'
    candle_scraper = CandleScraper(pyautogui, _symbol)
    chart_paginator = ChartPaginator(pyautogui)
    scraper = TickerSymbolScraper(chart_paginator, candle_scraper)
    scraper.scrape_candles_in_date_range(_symbol)
