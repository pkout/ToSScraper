import unittest
from pathlib import Path
from chart_paginator import ChartPaginator

from .misc import GuiControllerFake

FIXTURES_DIR = Path(__file__).parent / Path('fixtures')

class TestChartPaginator(unittest.TestCase):

    def setUp(self):
        self._fake_gui_controller_with_buffering_screen_followed_by_fully_loaded_chart_screen()
        self.paginator = ChartPaginator(self.mock_gui_controller)

    def _fake_gui_controller_with_buffering_screen_followed_by_fully_loaded_chart_screen(self):
        # Most tests don't use all successive screenshot() invocations.
        self.mock_gui_controller = GuiControllerFake(
            images_paths=[
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('chart-with-picker.jpg'),  # find day button
                FIXTURES_DIR / Path('prebuffering.jpg'),       # read status after clicking on Go button
                FIXTURES_DIR / Path('chart-with-picker.jpg')   # read status after clicking on Go button again
            ]
        )

    def test_instantiates(self):
        self.assertIsInstance(self.paginator, ChartPaginator)

    def test_next_page_clicks_on_date_picker_widget(self):
        expected_widget_coords = (2320, 58)

        self.paginator.next_page()

        self.assertIn(expected_widget_coords, self.mock_gui_controller.clicks)

    def test_next_page_clicks_on_next_month_button(self):
        expected_widget_coords = (2386, 91)

        self.paginator.next_page()

        self.assertIn(expected_widget_coords, self.mock_gui_controller.clicks)

    def test_next_page_clicks_on_first_open_market_day_of_month_button_in_date_picker(self):
        expected_btn_coords = (2259, 168)

        self.paginator.next_page()

        self.assertIn(expected_btn_coords, self.mock_gui_controller.clicks)

    def test_next_page_sets_11_59_pm_time_in_date_picker(self):
        expected_click_coords = (2270, 280)
        expected_right_arrow_key_presses = ('right', 8)
        expected_backspace_key_presses = ('backspace', 8)
        expected_typewrites = '23:59:00'

        self.paginator.next_page()

        self.assertIn(expected_click_coords, self.mock_gui_controller.clicks)
        self.assertIn(expected_right_arrow_key_presses, self.mock_gui_controller.presses)
        self.assertIn(expected_backspace_key_presses, self.mock_gui_controller.presses)
        self.assertIn(expected_typewrites, self.mock_gui_controller.typewrites)

    def test_next_page_clicks_on_go_button_in_date_picker(self):
        expected_click_coords = (2388, 288)

        self.paginator.next_page()

        self.assertIn(expected_click_coords, self.mock_gui_controller.clicks)

    def test_wait_for_buffering_to_finish_waits_until_buffering_process_finishes(self):
        self._fake_gui_controller_with_buffering_screen_followed_by_fully_loaded_chart_screen()
        self.paginator = ChartPaginator(self.mock_gui_controller)

        self.assertIsNone(self.paginator.state)

        self.paginator.next_page()

        self.assertEqual(self.paginator.state, 'Prebuffered')


