import shutil
from pathlib import Path

import utils
from screenshot_parsers import OHLCVParser, RSIParser
from settings import settings, profiled_settings
from log import logger

DIR = Path(__file__).parent

class CandleScraper:

    def __init__(self, gui_controller, ticker_symbol):
        self._gui_controller = gui_controller
        self._ticker_symbol = ticker_symbol
        self._determine_first_candle_center_coords()

    def scrape(self):
        self._move_mouse_before_first_candle()
        candle_values = {'ohlcv': [], 'rsi': []}

        for _ in self._move_cursor_towards_next_candle():
            ohlcv_image = self._screenshot_candle_ohlcv_text()
            rsi_image = self._screenshot_candle_rsi_text()

            if self._did_read_all_candles(ohlcv_image):
                break

            ohlcv = self._read_ohlcv_from(ohlcv_image)
            rsi = self._read_rsi_from(rsi_image)

            if self._is_candle_already_read(ohlcv, candle_values):
                continue

            candle_values['ohlcv'].append(ohlcv)
            candle_values['rsi'].append(rsi)

        return candle_values

    def _is_candle_already_read(self, candle, candle_values):
        timestamps = [k['t'] for k in candle_values['ohlcv']]

        candle_is_read = len(candle_values['ohlcv']) > 0 and \
            candle['t'] in timestamps

        return candle_is_read

    def _determine_first_candle_center_coords(self):
        _, screen_height = self._gui_controller.size()

        self._first_candle_center_xy = (
            profiled_settings['firstCandleCenterX'],
            screen_height / 2
        )

    def _move_mouse_before_first_candle(self):
        self._gui_controller.moveTo(
            self._first_candle_center_xy[0] - profiled_settings['candleWidthPx'],
            self._first_candle_center_xy[1],
            0
        )

    def _move_cursor_towards_next_candle(self):
        logger.info('Mouse stepping')

        for _ in range(settings['cursorStepsCount']):
            print('.', end='')

            self._gui_controller.moveRel(
                1, 0,
                duration=settings['cursorStepDurationSec']
            )

            yield

    def _screenshot_candle_ohlcv_text(self):
        r = profiled_settings['ohlcvScreenRegion']
        region_tuple = (r['x'], r['y'], r['w'], r['h'])
        image = self._gui_controller.screenshot(region=region_tuple)
        image = utils.sharpen_image(image, 5)
        image.save(DIR.parent / Path('last-ohlcv.png'))

        return image

    def _screenshot_candle_rsi_text(self):
        r = profiled_settings['rsiScreenRegion']
        region_tuple = (r['x'], r['y'], r['w'], r['h'])
        image = self._gui_controller.screenshot(region=region_tuple)
        image = utils.sharpen_image(image, 3)
        image.save(DIR.parent / Path('last-rsi.png'))

        return image

    def _did_read_all_candles(self, image):
        parser = OHLCVParser(image)

        return parser.is_past_last_ohlcv()

    def _read_ohlcv_from(self, image):
        parser = OHLCVParser(image)

        try:
            ohlcv = {
                't': parser.get_timestamp(),
                'o': parser.get_open(),
                'h': parser.get_high(),
                'l': parser.get_low(),
                'c': parser.get_close(),
                'v': parser.get_volume()
            }
        except ValueError as e:
            logger.error('OHLCV parsing error below. '
                         f'Timestamp {parser.get_timestamp()}')

            logger.error(e)

            shutil.copy(
                DIR.parent / Path('last-ohlcv.png'),
                DIR.parent / Path(f'ohlcv-{parser.get_timestamp()}.png')
            )

            ohlcv = {
                't': parser.get_timestamp(),
                'o': -1,
                'h': -1,
                'l': -1,
                'c': -1,
                'v': -1
            }

        return ohlcv

    def _read_rsi_from(self, image):
        parser = RSIParser(image)
        rsi_value = parser.get_rsi()

        if rsi_value is None:
            # This anomalous value will be easy to identify and replace
            # in the output file.
            rsi_value = -1

        rsi = {
            'rsi': rsi_value
        }

        return rsi