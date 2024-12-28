import json
import pyautogui

from pathlib import Path

from candle_scraper import CandleScraper

screen_width, screen_height = pyautogui.size() # Get the size of the primary monitor.


class TickerSymbolScraper:

    FIRST_CANDLE_COORDS = 300, screen_height / 2

    def __init__(self, candle_scraper):
        self._candle_scraper = candle_scraper

    def scrape_candles_in_date_range(self, symbol, start_datetime=None, end_datetime=None):
        candles_values = self._candle_scraper.scrape()

        return candles_values

    def save_to_file(self, _dict, path):
        if _dict is None:
            raise ValueError('The _dict argument cannot be None!')

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(_dict, f, indent=4)

def _save_file_path(symbol):
    Path('data').mkdir(parents=True, exist_ok=True)
    return Path(__file__).parent / Path('data') / Path(f'{symbol}.json')

if __name__ == '__main__':
    symbol = 'UVIX'

    candle_scraper = CandleScraper(
        gui_controller=pyautogui,
        ticker_symbol=symbol
    )

    scraper = TickerSymbolScraper(candle_scraper)
    candle_values = scraper.scrape_candles_in_date_range(symbol)
    scraper.save_to_file(candle_values, _save_file_path(symbol))
