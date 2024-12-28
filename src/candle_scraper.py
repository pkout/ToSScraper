from screenshot_parsers import OHLCVParser, RSIParser

from settings import settings
import image_utils

class CandleScraper:

    CANDLE_WIDTH_PX = 10
    CANDLE_STEPS_COUNT = 10000
    MOUSE_STEP_DURATION_SEC = 0.1

    def __init__(self, gui_controller, ticker_symbol):
        self._gui_controller = gui_controller
        self._ticker_symbol = ticker_symbol
        self._determine_first_candle_center_coords()

    def scrape(self):
        self._move_mouse_before_first_candle()
        candle_values = {'ohlcv': [], 'rsi': []}

        for _ in self._move_cursor_towards_next_candle():
            ohlcv_image = self._screenshot_candle_ohlcv_values()
            rsi_image = self._screenshot_candle_rsi_value()
            rsi_image = image_utils.sharpen(rsi_image, 3)

            if self._did_read_all_ohlcv(ohlcv_image):
                break

            ohlcv = self._read_ohlcv_from(ohlcv_image)
            rsi = self._read_rsi_from(rsi_image)

            if self._is_candle_already_read(ohlcv, candle_values):
                continue

            candle_values['ohlcv'].append(ohlcv)
            candle_values['rsi'].append(rsi)

        return candle_values

    def _is_candle_already_read(self, candle, candle_values):
        timestamps = [k['timestamp'] for k in candle_values['ohlcv']]

        candle_is_read = len(candle_values['ohlcv']) > 0 and \
            candle['timestamp'] in timestamps

        return candle_is_read

    def _determine_first_candle_center_coords(self):
        _, screen_height = self._gui_controller.size()
        self._first_candle_center_xy = 300, screen_height / 2

    def _move_mouse_before_first_candle(self):
        self._gui_controller.moveTo(
            self._first_candle_center_xy[0] - self.CANDLE_WIDTH_PX,
            self._first_candle_center_xy[1],
            0
        )

    def _move_cursor_towards_next_candle(self):
        print('Mouse stepping')

        for _ in range(self.CANDLE_STEPS_COUNT):
            print('.', end='')

            self._gui_controller.moveRel(
                1, 0,
                duration=self.MOUSE_STEP_DURATION_SEC
            )

            yield

    def _screenshot_candle_ohlcv_values(self):
        image = self._gui_controller.screenshot(region=(238, 125, 715, 15))
        image.save('last-ohlcv.png')

        return image

    def _screenshot_candle_rsi_value(self):
        image = self._gui_controller.screenshot(region=(430, 1042, 37, 17))
        image.save('last-rsi.png')

        return image

    def _did_read_all_ohlcv(self, image):
        parser = OHLCVParser(image)

        return parser.is_past_last_ohlcv()

    def _read_ohlcv_from(self, image):
        parser = OHLCVParser(image)

        ohlcv = {
            'timestamp': parser.get_timestamp(),
            'o': parser.get_open(),
            'h': parser.get_high(),
            'l': parser.get_low(),
            'c': parser.get_close(),
            'v': parser.get_volume()
        }

        return ohlcv

    def _read_rsi_from(self, image):
        parser = RSIParser(image)
        rsi_value = parser.get_rsi()

        if rsi_value is None:
            # This value will be easy to identify and replace
            # in the output file.
            rsi_value = -1

        rsi = {
            'rsi': rsi_value
        }

        return rsi