from pathlib import Path

from settings import profiled_settings

DIR = Path(__file__).parent

class FirstTradingDayOfMonthButtonNotFoundError(Exception):
    pass

class ChartPaginator:

    def __init__(self, gui_controller):
        self._gui_controller = gui_controller

    def next_page(self):
        self._move_cursor_over_date_picker_widget()
        day_btn_xy = self._find_first_market_open_day_of_month_button_center_xy()
        self._gui_controller.click(day_btn_xy)

    def _move_cursor_over_date_picker_widget(self):
        self._gui_controller.click(
            profiled_settings['calendarPickerCenterCoords']['x'],
            profiled_settings['calendarPickerCenterCoords']['y']
        )

    def _find_first_market_open_day_of_month_button_center_xy(self):
        # Indexed from 0
        for picker_row, picker_column in self._iterate_thru_14_days_buttons():
            x, y, w, h = self._get_button_bounding_box(picker_row,
                                                       picker_column)

            btn_screenshot = self._gui_controller.screenshot(
                region=(x, y, w, h)
            )

            save_file_path = DIR.parent / \
                Path(f'day_{picker_row}_{picker_column}.png')

            btn_screenshot.save(save_file_path)

            if self._is_first_market_open_day_button(btn_screenshot):
                btn_center_x = x + w // 2
                btn_center_y = y + h // 2

                return btn_center_x, btn_center_y

        raise FirstTradingDayOfMonthButtonNotFoundError()

    def _iterate_thru_14_days_buttons(self):
        for i in range(2):
            for j in range(7):
                yield i, j

    def _get_day_button_x(self, col_index):
        return profiled_settings['calendarPickerFirstDayRegion']['x'] + \
            (col_index * profiled_settings['calendarPickerFirstDayRegion']['w'])

    def _get_day_button_y(self, row_index):
        return profiled_settings['calendarPickerFirstDayRegion']['y'] + \
            (row_index * profiled_settings['calendarPickerFirstDayRegion']['h'])

    def _get_day_button_width(self):
        return profiled_settings['calendarPickerFirstDayRegion']['w']

    def _get_day_button_height(self):
        return profiled_settings['calendarPickerFirstDayRegion']['h']

    def _get_button_bounding_box(self, picker_row_idx, picker_column_idx):
        x = self._get_day_button_x(picker_column_idx)
        y = self._get_day_button_y(picker_row_idx)
        w = self._get_day_button_width()
        h = self._get_day_button_height()

        return x, y, w, h

    def _is_first_market_open_day_button(self, btn_screenshot):
        pixels = list(btn_screenshot.getdata())
        rs = [p[0] > 210 for p in pixels]
        gs = [p[1] > 210 for p in pixels]
        bs = [p[2] > 210 for p in pixels]
        result = any([True in rs, True in gs, True in bs])

        return result