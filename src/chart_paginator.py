from pathlib import Path

from screenshot_parsers import BufferingStatusParser
from settings import profiled_settings

DIR = Path(__file__).parent

class FirstTradingDayOfMonthButtonNotFoundError(Exception):
    pass

class ChartPaginator:

    def __init__(self, gui_controller):
        self._gui_controller = gui_controller
        self._state = None

    @property
    def state(self):
        return self._state

    def next_page(self):
        self._move_cursor_over_date_picker_widget()
        self._click_on_next_month_button()
        self._find_and_click_on_first_market_open_day_of_month_button()
        self._set_picker_time_to_11_59_pm()
        self._click_on_go_button()
        self._wait_for_buffering_to_finish()

    def _wait_for_buffering_to_finish(self):
        while True:
            self._state = 'Prebuffering'

            buffering_status_parser = BufferingStatusParser(
                self._find_buffering_status_image()
            )

            status = buffering_status_parser.get_buffering_status()

            if status != 'Prebuffering':
                self._state = 'Prebuffered'
                break

    def _find_buffering_status_image(self):
        r = profiled_settings['bufferingStatusRegion']
        region = r['x'], r['y'], r['w'], r['h']

        return self._gui_controller.screenshot(region=region)

    def _move_cursor_over_date_picker_widget(self):
        self._gui_controller.click(
            profiled_settings['calendarPickerCenterCoords']['x'],
            profiled_settings['calendarPickerCenterCoords']['y']
        )
    def _click_on_next_month_button(self):
        self._gui_controller.click(
            profiled_settings['calendarNextMonthButtonCenterCoords']['x'],
            profiled_settings['calendarNextMonthButtonCenterCoords']['y']
        )

    def _find_and_click_on_first_market_open_day_of_month_button(self):
        for picker_row_idx, picker_column_idx in self._iterate_14_days_of_buttons():
            x, y, w, h = self._get_button_bounding_box(
                picker_row_idx,
                picker_column_idx
            )

            btn_screenshot = self._gui_controller.screenshot(
                region=(x, y, w, h)
            )

            #save_file_path = DIR.parent / \
            #    Path(f'day_{picker_row_idx}_{picker_column_idx}.png')

            #btn_screenshot.save(save_file_path)

            if self._is_first_market_open_day_button(btn_screenshot):
                btn_center_x = x + w // 2
                btn_center_y = y + h // 2
                self._gui_controller.click(btn_center_x, btn_center_y)
                return

        raise FirstTradingDayOfMonthButtonNotFoundError()

    def _set_picker_time_to_11_59_pm(self):
        time_field_coords = profiled_settings['timeFieldInsideCoords']

        self._gui_controller.click(time_field_coords['x'],
                                   time_field_coords['y'])

        self._gui_controller.press('right', 8)
        self._gui_controller.press('backspace', 8)
        self._gui_controller.typewrite('23:59:00')

    def _click_on_go_button(self):
        self._gui_controller.click(
            profiled_settings['calendarGoButtonCenterCoords']['x'],
            profiled_settings['calendarGoButtonCenterCoords']['y']
        )

    def _iterate_14_days_of_buttons(self):
        for i in range(2):
            for j in range(7):
                yield i, j

    def _get_day_button_x(self, col_index):
        return profiled_settings['calendarFirstDayRegion']['x'] + \
            (col_index * self._get_day_button_width())

    def _get_day_button_y(self, row_index):
        return profiled_settings['calendarFirstDayRegion']['y'] + \
            (row_index * self._get_day_button_height())

    def _get_day_button_width(self):
        return profiled_settings['calendarFirstDayRegion']['w']

    def _get_day_button_height(self):
        return profiled_settings['calendarFirstDayRegion']['h']

    def _get_button_bounding_box(self, picker_row_idx, picker_column_idx):
        x = self._get_day_button_x(picker_column_idx)
        y = self._get_day_button_y(picker_row_idx)
        w = self._get_day_button_width()
        h = self._get_day_button_height()

        return x, y, w, h

    def _is_first_market_open_day_button(self, btn_screenshot):
        btn_pixels = list(btn_screenshot.getdata())
        rs = [p[0] > 210 for p in btn_pixels]
        gs = [p[1] > 210 for p in btn_pixels]
        bs = [p[2] > 210 for p in btn_pixels]
        result = all([True in rs, True in gs, True in bs])

        return result